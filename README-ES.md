For the English version, please click [here](README.md).

---

# Gemini Glow ✨

Un tema de alto contraste para Visual Studio Code, meticulosamente diseñado para replicar la vibrante y clara paleta de colores del código generado por Gemini más especificamente para codigo Python.

-----

## ¿Qué es Gemini Glow?

**Gemini Glow** nació de un objetivo simple: lograr una paridad visual casi perfecta entre el código de tu editor local y los fragmentos generados por Gemini. Si, como yo, disfrutas de la claridad y la estética de su resaltado de sintaxis, este tema es para ti.

Cada color ha sido cuidadosamente seleccionado para maximizar la legibilidad y reducir la fatiga visual, utilizando colores vibrantes para la sintaxis clave (funciones en amarillo, keywords en púrpura, tipos en verde) y tonos más sutiles para el resto del código, todo sobre un fondo oscuro y confortable.

## Así se vera tu codigo Python. Idem que en Gemini.

<img width="923" height="446" alt="image" src="https://github.com/user-attachments/assets/793d43f3-dd9e-4b7d-bbb9-e2d4b810b60a" />

-----

## ⚙️ Instalación

Puedes instalar **Gemini Glow** de dos maneras:

**1. Desde el Marketplace de VS Code (Recomendado)**

1.  Abre **Visual Studio Code**.
2.  Ve a la vista de **Extensiones** (`Ctrl+Shift+X`).
3.  Busca `Gemini Glow`.
4.  Haz clic en el botón **"Install"**.
5.  Activa el tema desde la Paleta de Comandos (`Ctrl+Shift+P`), buscando `Preferences: Color Theme` y seleccionando `Gemini Glow`.

**2. Desde la Paleta de Comandos**

1.  Abre la paleta de comandos (`Ctrl+P`).
2.  Pega el siguiente comando y presiona `Enter`:
    ```bash
    ext install GEMMA-CLAVERO-DEL-MORAL.gemini-glow
    ```
-----

## ✍️ Configuración Recomendada (¡Importante!)

Para una experiencia 100% fiel al estilo de Gemini, no solo importan los colores, sino también la fuente y la forma en que se renderizan ciertos caracteres.

**1. Fuente:** Recomiendo usar **Source Code Pro**, una fuente de código abierto de Google que es limpia y muy similar a la utilizada por Gemini.
**2. Ligaduras de Fuente:** Para obtener el efecto de guiones bajos separados (`__init__`) en lugar de una línea continua, es crucial desactivar las ligaduras y utilizar una fuente que lo permita.

Copia y adiciona a tu archivo `settings.json` la siguiente configuración (`Ctrl+Shift+P` > `Preferences: Open User Settings (JSON)`):

```json
    "editor.fontFamily": "Inconsolata, Consolas, 'Courier New', monospace",
    "editor.fontLigatures": false
```
## 💬 Feedback y Contribuciones
Este tema es un proyecto vivo. Si encuentras algún problema, un color que no se ve bien en algún lenguaje o tienes una sugerencia, por favor, abre un 'issue' en el repositorio de GitHub.

## Licencia
Este tema se distribuye bajo la **Licencia MIT**.
