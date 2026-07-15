# Release

Este projeto foi preparado para publicar no PyPI usando Trusted Publishing, sem token de longa duracao.

## Checklist local

Antes de criar uma tag:

```bash
python -m ruff check .
python -m pyright
python -m pytest --cov=notebookux --cov-report=term-missing
python -m build
python -m mkdocs build --strict
```

## Versionamento

1. Atualize `version` em `pyproject.toml`.
2. Atualize `__version__` em `src/notebookux/__init__.py`.
3. Atualize o teste de versionamento.
4. Confirme que a documentacao e o pacote constroem sem erro.

## Publicacao

Crie e envie uma tag:

```bash
git tag v0.1.0
git push origin v0.1.0
```

O workflow `.github/workflows/release.yml` constroi o pacote e publica no PyPI com `pypa/gh-action-pypi-publish@release/v1`.

## Configuracao no PyPI

No painel do projeto `notebookux` no PyPI, configure um Trusted Publisher com:

- repository owner: `jyrikes`
- repository name: `notebookux`
- workflow name: `release.yml`
- environment name: `pypi`

Essa configuracao e obrigatoria para que o workflow publique sem token.
