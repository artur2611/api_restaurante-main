from urllib.parse import urljoin

import requests
from requests.exceptions import RequestException
from django.conf import settings


class ApiClientError(Exception):
    """Raised for network or API client related errors."""


API_BASE = getattr(settings, 'FLASK_API_URL', 'http://localhost:5000')
TIMEOUT = settings.API_CLIENT.get('TIMEOUT', 5) if hasattr(settings, 'API_CLIENT') else 5


def _headers(token=None):
    headers = {'Content-Type': 'application/json'}
    if token:
        headers['Authorization'] = f'Bearer {token}'
    return headers


def _url(path: str) -> str:
    return urljoin(API_BASE.rstrip('/') + '/', path.lstrip('/'))


def login(username, password):
    # Try the common login paths: /login then /sesiones
    paths = ['login', 'sesiones']
    last_exc = None
    for p in paths:
        try:
            r = requests.post(_url(p), auth=(username, password), timeout=TIMEOUT)
        except RequestException as exc:
            last_exc = exc
            continue
        # If we got a response, evaluate it
        if r.status_code == 200:
            try:
                return r.json()
            except ValueError:
                raise ApiClientError('Login returned invalid JSON')
        # 401 -> invalid credentials, surface a clear error
        if r.status_code == 401:
            raise ApiClientError('Invalid credentials')
        # 404 -> try next path
        if r.status_code == 404:
            last_exc = RequestException(f'Path {p} not found (404)')
            continue
        # other errors
        raise ApiClientError(f'Login failed with status {r.status_code}')
    # If we exhausted paths, raise last network error if present
    if last_exc:
        raise ApiClientError('Failed to call login endpoint') from last_exc
    raise ApiClientError('Failed to call login endpoint')


def signup(username, email, password):
    try:
        # In your API users are created under /usuarios (POST)
        r = requests.post(_url('usuarios'), json={'nombre': username, 'email': email, 'password': password}, timeout=TIMEOUT)
        if r.status_code in (200, 201):
            return r.json()
        if r.status_code == 400:
            raise ApiClientError('Invalid signup data')
        raise ApiClientError(f'Signup failed with status {r.status_code}')
    except RequestException as exc:
        raise ApiClientError('Failed to call signup endpoint') from exc


def get_exercises(token, params=None):
    try:
        r = requests.get(_url('ejercicios'), headers=_headers(token), params=params or {}, timeout=TIMEOUT)
        r.raise_for_status()
        data = r.json()
        # Normalize to a list of ejercicios. API may return:
        # - a list directly
        # - a dict wrapper like {'ejercicios': [...]} or {'data': [...]} or {'results': [...]}
        # - a single object (one ejercicio)
        if isinstance(data, list):
            return data
        if isinstance(data, dict):
            for key in ('ejercicios', 'results', 'data', 'items'):
                if key in data and isinstance(data[key], list):
                    return data[key]
            for v in data.values():
                if isinstance(v, list):
                    return v
            # If we detect a single ejercicio object, wrap it
            if any(k in data for k in ('id', 'titulo', 'title', 'descripcion', 'description')):
                return [data]
            return []
        return []
    except RequestException as exc:
        raise ApiClientError('Failed to fetch ejercicios') from exc


def get_exercise(token, exercise_id):
    try:
        r = requests.get(_url(f'ejercicios/{exercise_id}'), headers=_headers(token), timeout=TIMEOUT)
        r.raise_for_status()
        return r.json()
    except RequestException as exc:
        raise ApiClientError('Failed to fetch ejercicio') from exc


def create_exercise(token, payload):
    try:
        r = requests.post(_url('ejercicios'), json=payload, headers=_headers(token), timeout=TIMEOUT)
        r.raise_for_status()
        return r.json()
    except RequestException as exc:
        raise ApiClientError('Failed to create ejercicio') from exc


def update_exercise(token, exercise_id, payload):
    try:
        r = requests.put(_url(f'ejercicios/{exercise_id}'), json=payload, headers=_headers(token), timeout=TIMEOUT)
        r.raise_for_status()
        return r.json()
    except RequestException as exc:
        raise ApiClientError('Failed to update ejercicio') from exc


def delete_exercise(token, exercise_id):
    try:
        r = requests.delete(_url(f'ejercicios/{exercise_id}'), headers=_headers(token), timeout=TIMEOUT)
        if r.status_code not in (200, 204):
            r.raise_for_status()
        return True
    except RequestException as exc:
        raise ApiClientError('Failed to delete ejercicio') from exc


# --- Usuarios (users) helpers ---
def get_users(token, params=None):
    try:
        r = requests.get(_url('usuarios'), headers=_headers(token), params=params or {}, timeout=TIMEOUT)
        r.raise_for_status()
        return r.json()
    except RequestException as exc:
        raise ApiClientError('Failed to fetch usuarios') from exc


def get_user(token, user_id):
    try:
        r = requests.get(_url(f'usuarios/{user_id}'), headers=_headers(token), timeout=TIMEOUT)
        r.raise_for_status()
        return r.json()
    except RequestException as exc:
        raise ApiClientError('Failed to fetch usuario') from exc


def create_user_public(payload):
    try:
        r = requests.post(_url('usuarios'), json=payload, timeout=TIMEOUT)
        r.raise_for_status()
        return r.json()
    except RequestException as exc:
        raise ApiClientError('Failed to create usuario') from exc


def update_user(token, user_id, payload):
    try:
        r = requests.put(_url(f'usuarios/{user_id}'), json=payload, headers=_headers(token), timeout=TIMEOUT)
        r.raise_for_status()
        return r.json()
    except RequestException as exc:
        raise ApiClientError('Failed to update usuario') from exc


def delete_user(token, user_id):
    try:
        r = requests.delete(_url(f'usuarios/{user_id}'), headers=_headers(token), timeout=TIMEOUT)
        if r.status_code not in (200, 204):
            r.raise_for_status()
        return True
    except RequestException as exc:
        raise ApiClientError('Failed to delete usuario') from exc
