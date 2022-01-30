import requests


def is_trello_board_name(key: str = "", token: str = "", board_name: str = "") -> bool:
    url = "https://api.trello.com/1/search"
    params = {
        "key": key,
        "token": token,
        "query": board_name,
        "modelTypes": "boards",
        "board_fields": "name",
        "boards_limit": 1,
    }
    headers = {"Accept": "application/json"}
    response = requests.request("GET", url, headers=headers, params=params)
    response.raise_for_status()
    if len(response.json()["boards"]) > 0:
        return True
    return False


def delete_trello_board(key: str = "", token: str = "", board_id: str = "") -> bool:
    url = f"https://api.trello.com/1/boards/{board_id}"
    params = {
        "key": key,
        "token": token,
    }
    response = requests.request("DELETE", url, params=params)
    response.raise_for_status()
    return True


def create_trello_board(key: str = "", token: str = "", payload: dict = {}) -> int:
    url = "https://api.trello.com/1/boards/"
    params = {
        "key": key,
        "token": token,
        **payload,
    }
    response = requests.request("POST", url, params=params)
    response.raise_for_status()
    board_id = response.json()["shortUrl"].split("/")[-1].strip()
    return board_id


def add_member_to_trello_board(
    key: str = "",
    token: str = "",
    board_id: str = "",
    member_id: str = "",
) -> bool:
    url = f"https://api.trello.com/1/boards/{board_id}/members/{member_id}"
    params = {
        "key": key,
        "token": token,
        "type": "normal",
    }
    response = requests.request("PUT", url, params=params)
    response.raise_for_status()
    return True


if __name__ == "__main__":
    from environs import Env

    env = Env()
    env.read_env("backend/.env")

    trello_key = env.str("TRELLO_KEY")
    trello_token = env.str("TRELLO_TOKEN")

    payload = {
        "name": "TestBoardMember",
        "prefs_background": "orange",
        "desc": "Доска для команды №",
    }

    is_board = is_trello_board_name(
        key=trello_key, token=trello_token, board_name=payload["name"]
    )

    if not is_board:
        trello_board_id = create_trello_board(
            key=trello_key,
            token=trello_token,
            payload=payload,
        )
        print(f"Создана доска с ID={trello_board_id}")
    else:
        print("Доска с таким названием уже существует.")

    add_member_to_trello_board(
        key=trello_key,
        token=trello_token,
        board_id=trello_board_id,
        member_id="denis60374775",
    )
