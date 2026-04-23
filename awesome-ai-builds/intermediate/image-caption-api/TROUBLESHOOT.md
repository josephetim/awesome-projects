# TROUBLESHOOT

## Slow startup

- First request loads BLIP-2 weights and processor.
- Keep model cached by running long-lived API workers.

## CUDA errors

- Set `BLIP_DEVICE=cpu` in `.env` to force CPU mode.
- If using GPU, verify CUDA-compatible torch build.

## Memory issues

- Use a smaller BLIP-2 model variant via `BLIP_MODEL_NAME`.
- Run on GPU with sufficient VRAM or increase host RAM for CPU mode.
