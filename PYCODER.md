# pycoder

pycoder is a Python IDE built from the PyCharm Community sources in
[JetBrains/intellij-community](https://github.com/JetBrains/intellij-community)
(Apache 2.0). It is not affiliated with or endorsed by JetBrains. PyCharm and
IntelliJ are trademarks of JetBrains s.r.o.

## Branches

- `master` tracks `upstream/master` (JetBrains) unchanged.
- `pycoder` holds the pycoder changes on top of it.

## Build

```bash
./build/run_build_target.sh . //python/build:i_build_target -Dintellij.build.target.os=current
```

Installers land in `out/`. The first build downloads Bazel and dependencies and
takes over an hour; 16 GB of RAM is recommended.

## Branding

`pycoder-branding/generate.py` regenerates every product image (icons, splash,
installer artwork) into `python/resources` and `python/build/images`:

```bash
python3 pycoder-branding/generate.py
```

The product name, icons and splash are set in
`python/ide-common/resources/idea/PyCharmCoreApplicationInfo.xml`; installer
names, bundle id and config directory (`pycoder<version>`) in
`python/build/src/org/jetbrains/intellij/build/pycharm/PyCharmCommunityProperties.kt`.

The product code stays `PC` (PyCharm Community) so the Marketplace keeps
offering the same compatible plugins.

## Syncing with upstream

```bash
git fetch upstream master
git checkout pycoder && git merge upstream/master
```
