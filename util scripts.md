## OnCreated
```python
node = kwargs["node"]
node.hdaModule().init(node)
```
## Callbacks
```python
hou.phm().add_shot(kwargs["node"])                  # Add Shot
hou.phm().remove_shot(kwargs["node"])               # Remove Shot
hou.phm().sync_ui(kwargs["node"])                   # Shot Index, internal func
hou.phm().store_current_shot(kwargs["node"])        # all shot data parameters
hou.phm().render_all(kwargs["node"])                # Render All
hou.phm().render_current(kwargs["node"])            # Render Current
```
## Other
### Font setups
```C
`chs("../../../primary_action")`

s@main_action = chs("Text");
f@scale_mult = 0;

i@textlength = strlen(@main_action);
if (@textlength >= 37){
    f@scale_mult = (@textlength - 37) * 0.0015;
}
```
then in [font] COP:
```C
// Text
`details(-1, "text")`

// scale X
0.044 - detail("../../../../Shot_00/Text/audio_notes_setup", "scale_mult", 0)
```
### Extra File pngs
```C
opdef:../..?additionalnotes.png
```
### ROP export path
```C
`chs("../../export_dir")``chs("../../export_filename")`.sh`chs("../../shot_index")`.png
```
