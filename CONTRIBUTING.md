# Contributing

Script Packs execute inside Host Apps, so each change is supply-chain sensitive.

Required gates:

- Review every pack change before consumption.
- Keep locked environments resolved at bind time.
- Pin consumed packs by `name`, `version`, and `contentHash`.
- Do not commit secrets, compiled binaries, virtual environments, downloaded model weights, or Homebrew/system assets.
- Keep copyleft or system dependencies as declarations only unless a licence review explicitly permits bundling.
- Keep managed assets behind explicit consent text, declared size, source, and checksum.

Mode-2 and mode-3 install execution are out of scope for this repository until Bridle v0.4.
