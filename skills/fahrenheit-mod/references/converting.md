# Converting existing mods

Mods made with other loaders can move to Fahrenheit. Converting keeps one
ecosystem for players.

## External File Loader mods

ffgriever's External File Loader (EFL) mods replace archive files. When
Fahrenheit runs, its own file loader takes over and the standalone EFL is
not used.

1. Create a mod folder named after a new mod ID.
2. Move the replacement files to `efl/x/...` (FFX) or `efl/x2/...` (X-2),
   keeping their path inside the archive.
3. Write `<mod_id>.manifest.json` by hand
   ([structure.md](structure.md)).
4. Ask the original author before redistributing their files.

## ASI, dinput8/version proxy and injector mods

These run native code inside the game. Rewrite the behaviour as a Fahrenheit
code mod:

1. List every function the old mod hooks or calls, with its address and
   signature, and every memory location it reads or writes.
2. Check that the addresses are for the same game build that the target
   Fahrenheit version supports ([versions.md](versions.md)). Addresses from
   the 2019 build do not apply to the 2026 build.
3. Turn each hook into an `FhCallHandle<T>` hook in `init`
   ([calls.md](calls.md)), chaining to the original.
4. Replace direct memory pokes with call hooks where possible; where not, read
   and write through pointers obtained after `init`, relative to the module
   base.
5. Move any config file into Fahrenheit settings, and any extra save data into
   local state ([runtime.md](runtime.md)).
6. Remove the proxy DLL and any files the old mod put in the game folder.

## Standalone tools that patch game files on disk

Keep the tool if it is useful for authoring, but have it output a Fahrenheit
file mod (`efl` folder plus manifest) instead of overwriting the archives or
writing into the game folder.
