import os
import json
import sqlite3
from http import HTTPStatus
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from datetime import datetime
from urllib.parse import urlparse


BASE_DIR = Path(__file__).parent
FRONTEND_DIR = BASE_DIR / "frontend"
DB_PATH = BASE_DIR / "academia.db"


DEFAULT_MACHINES = [
    {
        "id": 1,
        "nome": "Esteira Profissional",
        "status": "operando",
        "localizacao": "Sala Cardio",
        "ultima_manutencao": "2026-03-10",
        "observacao": "Funcionando normalmente.",
    },
    {
        "id": 2,
        "nome": "Bicicleta Ergometrica",
        "status": "com problema",
        "localizacao": "Sala Cardio",
        "ultima_manutencao": "2026-02-22",
        "observacao": "Painel intermitente. Aguardando revisao.",
    },
    {
        "id": 3,
        "nome": "Supino Articulado",
        "status": "operando",
        "localizacao": "Sala Musculacao",
        "ultima_manutencao": "2026-03-28",
        "observacao": "Sem ocorrencias.",
    },
    {
        "id": 4,
        "nome": "Leg Press 45",
        "status": "com problema",
        "localizacao": "Sala Musculacao",
        "ultima_manutencao": "2026-01-30",
        "observacao": "Barulho anormal no trilho.",
    },
]

ALLOWED_MACHINE_STATUSES = {"operando", "com problema", "fora de servico"}


STUDENTS = {
    "1001": {
        "nome": "Ana Souza",
        "mensalidade": "paga",
        "vencimento": "2026-04-10",
        "referencia": "Abril/2026",
    },
    "1002": {
        "nome": "Carlos Lima",
        "mensalidade": "atrasada",
        "vencimento": "2026-03-10",
        "referencia": "Marco/2026",
    },
    "1003": {
        "nome": "Fernanda Alves",
        "mensalidade": "paga",
        "vencimento": "2026-04-05",
        "referencia": "Abril/2026",
    },
    "1004": {
        "nome": "Joao Pereira",
        "mensalidade": "atrasada",
        "vencimento": "2026-03-25",
        "referencia": "Marco/2026",
    },
}


def get_db_connection():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def init_db():
    with get_db_connection() as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS academy_state (
                id INTEGER PRIMARY KEY CHECK (id = 1),
                people_count INTEGER NOT NULL DEFAULT 0 CHECK (people_count >= 0)
            )
            """
        )
        connection.execute(
            """
            INSERT INTO academy_state (id, people_count)
            VALUES (1, 0)
            ON CONFLICT(id) DO NOTHING
            """
        )
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS machine_notes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                machine_id INTEGER NOT NULL,
                autor TEXT NOT NULL,
                tipo TEXT NOT NULL,
                mensagem TEXT NOT NULL,
                criado_em TEXT NOT NULL
            )
            """
        )
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS machine_status (
                machine_id INTEGER PRIMARY KEY,
                status TEXT NOT NULL
            )
            """
        )
        columns = {
            row["name"] for row in connection.execute("PRAGMA table_info(machine_status)")
        }
        if "ultima_manutencao" not in columns:
            connection.execute(
                "ALTER TABLE machine_status ADD COLUMN ultima_manutencao TEXT"
            )
        if "observacao" not in columns:
            connection.execute(
                "ALTER TABLE machine_status ADD COLUMN observacao TEXT"
            )
        connection.executemany(
            """
            INSERT INTO machine_status (machine_id, status, ultima_manutencao, observacao)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(machine_id) DO NOTHING
            """,
            [
                (
                    machine["id"],
                    machine["status"],
                    machine["ultima_manutencao"],
                    machine["observacao"],
                )
                for machine in DEFAULT_MACHINES
            ],
        )
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS machines (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                status TEXT NOT NULL,
                localizacao TEXT NOT NULL,
                ultima_manutencao TEXT NOT NULL,
                observacao TEXT NOT NULL
            )
            """
        )
        if connection.execute("SELECT COUNT(*) FROM machines").fetchone()[0] == 0:
            for machine in DEFAULT_MACHINES:
                legacy_row = connection.execute(
                    """
                    SELECT status, ultima_manutencao, observacao
                    FROM machine_status
                    WHERE machine_id = ?
                    """,
                    (machine["id"],),
                ).fetchone()
                connection.execute(
                    """
                    INSERT INTO machines (id, nome, status, localizacao, ultima_manutencao, observacao)
                    VALUES (?, ?, ?, ?, ?, ?)
                    """,
                    (
                        machine["id"],
                        machine["nome"],
                        legacy_row["status"] if legacy_row and legacy_row["status"] else machine["status"],
                        machine["localizacao"],
                        legacy_row["ultima_manutencao"] if legacy_row and legacy_row["ultima_manutencao"] else machine["ultima_manutencao"],
                        legacy_row["observacao"] if legacy_row and legacy_row["observacao"] else machine["observacao"],
                    ),
                )
        connection.commit()


def get_people_count():
    with get_db_connection() as connection:
        row = connection.execute(
            "SELECT people_count FROM academy_state WHERE id = 1"
        ).fetchone()
        return row["people_count"] if row else 0


def update_people_count(delta):
    with get_db_connection() as connection:
        current = connection.execute(
            "SELECT people_count FROM academy_state WHERE id = 1"
        ).fetchone()
        current_value = current["people_count"] if current else 0
        new_value = current_value + delta

        if new_value < 0:
            return None

        connection.execute(
            "UPDATE academy_state SET people_count = ? WHERE id = 1",
            (new_value,),
        )
        connection.commit()
        return new_value


def list_machines():
    with get_db_connection() as connection:
        rows = connection.execute(
            """
            SELECT id, nome, status, localizacao, ultima_manutencao, observacao
            FROM machines
            ORDER BY id
            """,
        ).fetchall()
        return [dict(row) for row in rows]


def get_machine_by_id(machine_id):
    with get_db_connection() as connection:
        row = connection.execute(
            """
            SELECT id, nome, status, localizacao, ultima_manutencao, observacao
            FROM machines
            WHERE id = ?
            """,
            (machine_id,),
        ).fetchone()
        return dict(row) if row else None


def update_machine_details(machine_id, status, ultima_manutencao, observacao):
    with get_db_connection() as connection:
        connection.execute(
            """
            UPDATE machines
            SET status = ?, ultima_manutencao = ?, observacao = ?
            WHERE id = ?
            """,
            (status, ultima_manutencao, observacao, machine_id),
        )
        connection.commit()


def get_machine_notes(machine_id):
    with get_db_connection() as connection:
        rows = connection.execute(
            """
            SELECT id, machine_id, autor, tipo, mensagem, criado_em
            FROM machine_notes
            WHERE machine_id = ?
            ORDER BY id DESC
            """,
            (machine_id,),
        ).fetchall()
        return [dict(row) for row in rows]


def add_machine_note(machine_id, autor, tipo, mensagem):
    criado_em = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with get_db_connection() as connection:
        cursor = connection.execute(
            """
            INSERT INTO machine_notes (machine_id, autor, tipo, mensagem, criado_em)
            VALUES (?, ?, ?, ?, ?)
            """,
            (machine_id, autor, tipo, mensagem, criado_em),
        )
        connection.commit()
        note_id = cursor.lastrowid

    return {
        "id": note_id,
        "machine_id": machine_id,
        "autor": autor,
        "tipo": tipo,
        "mensagem": mensagem,
        "criado_em": criado_em,
    }


def delete_machine_note(machine_id, note_id):
    with get_db_connection() as connection:
        cursor = connection.execute(
            """
            DELETE FROM machine_notes
            WHERE id = ? AND machine_id = ?
            """,
            (note_id, machine_id),
        )
        connection.commit()
        return cursor.rowcount > 0


def create_machine(nome, status, ultima_manutencao, observacao, localizacao="Nao informada"):
    with get_db_connection() as connection:
        cursor = connection.execute(
            """
            INSERT INTO machines (nome, status, localizacao, ultima_manutencao, observacao)
            VALUES (?, ?, ?, ?, ?)
            """,
            (nome, status, localizacao, ultima_manutencao, observacao),
        )
        connection.commit()
        return cursor.lastrowid


def delete_machine(machine_id):
    with get_db_connection() as connection:
        connection.execute(
            "DELETE FROM machine_notes WHERE machine_id = ?",
            (machine_id,),
        )
        connection.execute(
            "DELETE FROM machine_status WHERE machine_id = ?",
            (machine_id,),
        )
        cursor = connection.execute(
            "DELETE FROM machines WHERE id = ?",
            (machine_id,),
        )
        connection.commit()
        return cursor.rowcount > 0


class GymRequestHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(FRONTEND_DIR), **kwargs)

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path

        if path == "/api/pessoas":
            self.send_json({"people_count": get_people_count()})
            return

        if path == "/api/maquinas":
            self.send_json(list_machines())
            return

        if path.startswith("/api/maquinas/"):
            machine_id = path.removeprefix("/api/maquinas/")
            if not machine_id.isdigit():
                self.send_json({"erro": "Identificador de maquina invalido."}, HTTPStatus.BAD_REQUEST)
                return

            machine = get_machine_by_id(int(machine_id))
            if not machine:
                self.send_json({"erro": "Maquina nao encontrada."}, HTTPStatus.NOT_FOUND)
                return

            payload = dict(machine)
            payload["anotacoes"] = get_machine_notes(int(machine_id))
            self.send_json(payload)
            return

        if path.startswith("/api/mensalidades/"):
            registration = path.removeprefix("/api/mensalidades/")
            student = STUDENTS.get(registration)
            if not student:
                self.send_json({"erro": "Matricula nao encontrada."}, HTTPStatus.NOT_FOUND)
                return

            payload = {
                "matricula": registration,
                "nome": student["nome"],
                "mensalidade": student["mensalidade"],
                "vencimento": student["vencimento"],
                "referencia": student["referencia"],
            }
            self.send_json(payload)
            return

        if path == "/":
            self.path = "/index.html"

        super().do_GET()

    def do_POST(self):
        parsed = urlparse(self.path)
        path = parsed.path

        if path == "/api/pessoas/entrada":
            updated_count = update_people_count(1)
            self.send_json({"people_count": updated_count})
            return

        if path == "/api/pessoas/saida":
            updated_count = update_people_count(-1)
            if updated_count is None:
                self.send_json(
                    {"erro": "A contagem ja esta em zero e nao pode ficar negativa."},
                    HTTPStatus.BAD_REQUEST,
                )
                return

            self.send_json({"people_count": updated_count})
            return

        if path == "/api/maquinas":
            payload = self.read_json_body()
            nome = str(payload.get("nome", "")).strip()
            status = str(payload.get("status", "")).strip().lower()
            ultima_manutencao = str(payload.get("ultima_manutencao", "")).strip()
            observacao = str(payload.get("observacao", "")).strip()
            localizacao = str(payload.get("localizacao", "Nao informada")).strip() or "Nao informada"

            if not nome:
                self.send_json({"erro": "Informe o nome da nova maquina."}, HTTPStatus.BAD_REQUEST)
                return

            if status not in ALLOWED_MACHINE_STATUSES:
                self.send_json({"erro": "Status da maquina invalido."}, HTTPStatus.BAD_REQUEST)
                return

            if not ultima_manutencao:
                self.send_json({"erro": "Informe a data da manutencao."}, HTTPStatus.BAD_REQUEST)
                return

            if not observacao:
                self.send_json({"erro": "Informe a observacao do equipamento."}, HTTPStatus.BAD_REQUEST)
                return

            machine_id = create_machine(nome, status, ultima_manutencao, observacao, localizacao)
            created_machine = get_machine_by_id(machine_id)
            created_machine["anotacoes"] = []
            self.send_json(created_machine, HTTPStatus.CREATED)
            return

        if path.startswith("/api/maquinas/") and path.endswith("/anotacoes"):
            machine_id = path.removeprefix("/api/maquinas/").removesuffix("/anotacoes")
            if not machine_id.isdigit():
                self.send_json({"erro": "Identificador de maquina invalido."}, HTTPStatus.BAD_REQUEST)
                return

            machine_id = int(machine_id)
            machine = get_machine_by_id(machine_id)
            if not machine:
                self.send_json({"erro": "Maquina nao encontrada."}, HTTPStatus.NOT_FOUND)
                return

            payload = self.read_json_body()
            autor = str(payload.get("autor", "")).strip()
            tipo = str(payload.get("tipo", "")).strip().lower()
            mensagem = str(payload.get("mensagem", "")).strip()

            if not autor:
                self.send_json({"erro": "Informe o nome do aluno."}, HTTPStatus.BAD_REQUEST)
                return

            if tipo not in {"anotacao", "defeito"}:
                self.send_json({"erro": "Tipo de relato invalido."}, HTTPStatus.BAD_REQUEST)
                return

            if not mensagem:
                self.send_json({"erro": "Escreva a anotacao ou defeito encontrado."}, HTTPStatus.BAD_REQUEST)
                return

            note = add_machine_note(machine_id, autor, tipo, mensagem)
            self.send_json(note, HTTPStatus.CREATED)
            return

        if path.startswith("/api/maquinas/") and path.endswith("/status"):
            machine_id = path.removeprefix("/api/maquinas/").removesuffix("/status")
            if not machine_id.isdigit():
                self.send_json({"erro": "Identificador de maquina invalido."}, HTTPStatus.BAD_REQUEST)
                return

            machine_id = int(machine_id)
            machine = get_machine_by_id(machine_id)
            if not machine:
                self.send_json({"erro": "Maquina nao encontrada."}, HTTPStatus.NOT_FOUND)
                return

            payload = self.read_json_body()
            status = str(payload.get("status", "")).strip().lower()
            ultima_manutencao = str(payload.get("ultima_manutencao", "")).strip()
            observacao = str(payload.get("observacao", "")).strip()

            if status not in ALLOWED_MACHINE_STATUSES:
                self.send_json({"erro": "Status da maquina invalido."}, HTTPStatus.BAD_REQUEST)
                return

            if not ultima_manutencao:
                self.send_json({"erro": "Informe a data da manutencao."}, HTTPStatus.BAD_REQUEST)
                return

            if not observacao:
                self.send_json({"erro": "Informe a observacao do equipamento."}, HTTPStatus.BAD_REQUEST)
                return

            update_machine_details(machine_id, status, ultima_manutencao, observacao)
            updated_machine = get_machine_by_id(machine_id)
            updated_machine["anotacoes"] = get_machine_notes(machine_id)
            self.send_json(updated_machine)
            return

        self.send_json({"erro": "Rota nao encontrada."}, HTTPStatus.NOT_FOUND)

    def do_DELETE(self):
        parsed = urlparse(self.path)
        path = parsed.path

        if path.startswith("/api/maquinas/") and "/anotacoes/" in path:
            prefix, note_id = path.split("/anotacoes/", 1)
            machine_id = prefix.removeprefix("/api/maquinas/")

            if not machine_id.isdigit() or not note_id.isdigit():
                self.send_json({"erro": "Identificador invalido."}, HTTPStatus.BAD_REQUEST)
                return

            removed = delete_machine_note(int(machine_id), int(note_id))
            if not removed:
                self.send_json({"erro": "Anotacao nao encontrada."}, HTTPStatus.NOT_FOUND)
                return

            self.send_json({"ok": True})
            return

        if path.startswith("/api/maquinas/"):
            machine_id = path.removeprefix("/api/maquinas/")
            if not machine_id.isdigit():
                self.send_json({"erro": "Identificador invalido."}, HTTPStatus.BAD_REQUEST)
                return

            removed = delete_machine(int(machine_id))
            if not removed:
                self.send_json({"erro": "Maquina nao encontrada."}, HTTPStatus.NOT_FOUND)
                return

            self.send_json({"ok": True})
            return

        self.send_json({"erro": "Rota nao encontrada."}, HTTPStatus.NOT_FOUND)

    def read_json_body(self):
        content_length = int(self.headers.get("Content-Length", "0"))
        if content_length <= 0:
            return {}

        raw_body = self.rfile.read(content_length)
        if not raw_body:
            return {}

        try:
            return json.loads(raw_body.decode("utf-8"))
        except json.JSONDecodeError:
            return {}

    def send_json(self, payload, status=HTTPStatus.OK):
        response = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, DELETE, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Content-Length", str(len(response)))
        self.end_headers()
        self.wfile.write(response)

    def do_OPTIONS(self):
        self.send_response(HTTPStatus.NO_CONTENT)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, DELETE, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()


def run(server_class=ThreadingHTTPServer, handler_class=GymRequestHandler):
    init_db()
    port = int(os.environ.get("PORT", "8000"))
    server = server_class(("127.0.0.1", port), handler_class)
    print(f"Servidor em http://127.0.0.1:{port}")
    server.serve_forever()


if __name__ == "__main__":
    run()
