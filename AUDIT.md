# Auditoría y plan de refactorización

Resumen de decisiones iniciales:
- GUI: usar `tkinter` (ligero, incluido en stdlib). Si prefieres otra, indícalo.
- Inferencia: usar `ultralytics` (instancia `YOLO`) y `model.predict`.
- Captura: usar API de Windows + `Pillow`/`mss` para capturar la ventana de `wakfu.exe`.
- Clicks: usar `pyautogui` para mover cursor y simular clicks.
- Notificaciones: usar `win10toast` (alternativa `plyer` si falla).
- Concurrency: hilo/worker asíncrono simple con un flag `processing_image` para asegurar que solo una imagen se procese a la vez.
- Threshold: filtrar detecciones con `confidence >= 0.85` (configurable en `.env`).

Archivos propuestos a ELIMINAR (según la especificación):
- `scripts/data_augmentation.py`  (eliminar)
- `scripts/run_yolo.py`          (eliminar)

Archivos a mantener o refactorizar:
- `scripts/train_yolo.py` -> mantener y refactorizar como script independiente + su propio `.env` en `scripts/`.
- `libs/` -> revisar y migrar utilidades necesarias a `app/utils.py` o módulos específicos.
- `run.py` -> reemplazar por `app/main.py` que arranque la GUI.

Nueva estructura propuesta:
```
app/
  __init__.py
  main.py            # arranque de la app (GUI)
  ui.py              # widgets y layout (Tkinter)
  capture.py         # captura de ventana wakfu.exe
  yolo_wrapper.py    # carga y predict del modelo YOLO
  processor.py       # cálculo de centros, overlay, lógica de acciones
  actions.py         # simulación de clicks y control de flags
  notifier.py        # notificaciones Windows
  config.py          # carga .env y constantes
tests/
scripts/
  train_yolo.py      # script independiente y simple
train_data/          # mantenida con .gitignore + .gitkeep
requirements.txt     # actualizar con las dependencias finales
```

Puntos críticos / riesgos (confirmados y mitigaciones):
- Captura: `wakfu.exe` es Java — debería poder capturarse con `mss` o `win32gui` (no DirectX exclusivo). Si la captura falla en ciertos entornos, habrá que usar técnicas alternativas.
- Simulación de clicks: `pyautogui` mueve y hace click; si el proceso requiere privilegios se necesitarán elevar permisos.
- Rendimiento: proteger la GUI evitando bloqueo con un worker thread y el flag `processing_image`.
- Escalado de coordenadas: siempre mapear boxes desde la imagen procesada (original) al preview (450x250) con factores de escala bien definidos.
- Umbral de confianza: aplicar `0.85` por defecto, configurable vía `.env`.

Siguientes pasos propuestos (ejecución):
1. Implementar `app/config.py` que lea `.env` del root para la GUI.
2. Implementar `app/capture.py` (función `capture_wakfu_window()`).
3. Implementar `app/yolo_wrapper.py` (clase `YoloModel` con `load()` y `predict()` que devuelva boxes filtrados por threshold).
4. Implementar `app/processor.py` (centros, overlay con cajas o centros aleatorios cuando corresponda).
5. Implementar `app/ui.py` y `app/main.py` para la ventana Tkinter con el layout especificado.
6. Refactorizar `scripts/train_yolo.py` y añadir `scripts/.env`.

Antes de modificar código: confirmar que aceptas `tkinter`, `pyautogui`, `ultralytics`, `python-dotenv`, `mss`, `Pillow`, `win10toast` como dependencias sugeridas.
