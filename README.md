# A2: Infraestructura i Arquitectura
Desplegament de Infraestructura i Arquitectura.

## Este repo usa flake8 como linter

### Local
Puedes correr flake8 en local ejecutando desde el root del repo el siguiente commando:

```bash
make linter
```

### Gitub Action
En cada pull request hay una github actions que saltara en cada commit y pasara el linter. se añade como un check que debes pasar para mergear el PR

