## driftfix: pydantic

**❌ Not fixed** · cost $3.09

Agent stopped: `Claude Code returned an error result: Reached maximum budget ($3) (exit code: 1)`

Tests still failing:
```

E   
E   For further information visit https://errors.pydantic.dev/2.13/u/removed-kwargs
____________ ERROR collecting tests/functional/test_docs_linting.py ____________
tests/functional/test_docs_linting.py:14: in <module>
    from antsibull_docs.cli.antsibull_docs import run
src/antsibull_docs/cli/antsibull_docs.py:43: in <module>
    from ..schemas.app_context import DocsAppContext  # noqa: E402
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
src/antsibull_docs/schemas/app_context.py:18: in <module>
    DOC_PARSING_BACKEND_CHOICES_F = p.Field("auto", regex="^(auto|ansible-core-2\\.13)$")
                                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
../venv/lib/python3.12/site-packages/pydantic/fields.py:1323: in Field
    raise PydanticUserError('`regex` is removed. use `pattern` instead', code='removed-kwargs')
E   pydantic.errors.PydanticUserError: `regex` is removed. use `pattern` instead
E   
E   For further information visit https://errors.pydantic.dev/2.13/u/removed-kwargs
________ ERROR collecting tests/functional/test_sphinx_init_baseline.py ________
tests/functional/test_sphinx_init_baseline.py:15: in <module>
    from antsibull_docs.cli.antsibull_docs import run
src/antsibull_docs/cli/antsibull_docs.py:43: in <module>
    from ..schemas.app_context import DocsAppContext  # noqa: E402
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
src/antsibull_docs/schemas/app_context.py:18: in <module>
    DOC_PARSING_BACKEND_CHOICES_F = p.Field("auto", regex="^(auto|ansible-core-2\\.13)$")
                                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
../venv/lib/python3.12/site-packages/pydantic/fields.py:1323: in Field
    raise PydanticUserError('`regex` is removed. use `pattern` instead', code='removed-kwargs')
E   pydantic.errors.PydanticUserError: `regex` is removed. use `pattern` instead
E   
E   For further information visit https://errors.pydantic.dev/2.13/u/removed-kwargs
=========================== short test summary info ============================
ERROR tests/functional/schema/test_schema.py - pydantic.errors.PydanticUserError: `regex` is removed. use `pattern` instead

For further information visit https://errors.pydantic.dev/2.13/u/removed-kwargs
ERROR tests/functional/test_docs_baseline.py - pydantic.errors.PydanticUserError: `regex` is removed. use `pattern` instead

For further information visit https://errors.pydantic.dev/2.13/u/removed-kwargs
ERROR tests/functional/test_docs_linting.py - pydantic.errors.PydanticUserError: `regex` is removed. use `pattern` instead

For further information visit https://errors.pydantic.dev/2.13/u/removed-kwargs
ERROR tests/functional/test_sphinx_init_baseline.py - pydantic.errors.PydanticUserError: `regex` is removed. use `pattern` instead

For further information visit https://errors.pydantic.dev/2.13/u/removed-kwargs
!!!!!!!!!!!!!!!!!!! Interrupted: 4 errors during collection !!!!!!!!!!!!!!!!!!!!
27 deselected, 4 errors in 0.29s
```
