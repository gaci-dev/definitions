# Instalacion organizacional en ChatGPT Business

Este directorio es un marketplace de plugins para ChatGPT y Codex. Debe publicarse dentro de un repositorio de GitHub accesible para un administrador del workspace.

## Importar desde GitHub

1. En ChatGPT, cambie al workspace Business de la organizacion.
2. Abra `Workspace settings > Plugins`.
3. Seleccione `Add > Import marketplace`.
4. Complete:
   - Source: `https://github.com/gaci-dev/definitions`
   - Path: `codex-marketplace`
   - Branch: `main`
5. Seleccione `Import marketplace` y autorice el acceso de GitHub.
6. Abra el plugin `gaci-documentacion-genexus`.
7. Establezca `Installation policy` en `Installed` para que quede instalado automaticamente para los miembros elegibles.
8. En `Workspace settings > Apps`, habilite GitHub y defina el acceso permitido. Los permisos efectivos sobre cada repositorio siguen siendo los de cada usuario en GitHub.

Las actualizaciones se sincronizan diariamente. Para solicitar una actualizacion inmediata use `Workspace settings > Plugins > Marketplaces > Gaci > Sync now`.

## Uso

En ChatGPT, mencione el plugin o seleccionelo desde el menu de herramientas:

```text
@Documentacion GeneXus Gaci analiza este repositorio o XPZ y genera la documentacion corporativa.
```

En Codex, abra `Sources > Use plugins` y seleccione `Documentacion GeneXus Gaci`.

## Contenido

- `documentacion-tecnica-gaci`: genera JSON, PDF y DOCX con el generador corporativo incluido.
- `xpz-analyzer`: analiza XPZ en modo de solo lectura.
- `nexa`: conocimiento de objetos, codigo y modelado GeneXus.
- Skills especializadas de SAP, Chameleon, Mercury, sistemas de diseno y generacion de UI.

La importacion, compilacion o ejecucion de un XPZ en una Knowledge Base requiere un pedido y autorizacion explicitos.
