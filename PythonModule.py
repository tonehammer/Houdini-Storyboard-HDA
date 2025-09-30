import json
import hou

def init(hda_node):
    """Initializes the first shot with default values from the HDA parameters."""
    default_shot = {
        "shot_number": hda_node.parm("shot_number").eval(),
        "shot_description": hda_node.parm("shot_description").eval(),
        "primary_action": hda_node.parm("primary_action").eval(),
        "secondary_action": hda_node.parm("secondary_action").eval(),
        "dialogue": hda_node.parm("dialogue").eval(),
        "acting_notes": hda_node.parm("acting_notes").eval(),
        "additional_notes": hda_node.parm("additional_notes").eval(),
        "audio_notes": hda_node.parm("audio_notes").eval(),
        "add_image": hda_node.parm("add_image").eval(),
        "use_img_as_background": hda_node.parm("use_img_as_background").eval(),
        "image_opacity": hda_node.parm("image_opacity").eval(),
        "image_type": hda_node.parm("image_type").eval(),
        "image_dir": hda_node.parm("image_dir").eval(),
        "snapshot_dir": hda_node.parm("snapshot_dir").eval(),
        "image_translatex": hda_node.parm("image_translatex").eval(),
        "image_translatey": hda_node.parm("image_translatey").eval(),
        "image_scalex": hda_node.parm("image_scalex").eval(),
        "image_scaley": hda_node.parm("image_scaley").eval(),
        "add_title_screen": hda_node.parm("add_title_screen").eval()
    }

    hda_node.parm("shot_data").set(json.dumps([default_shot], indent=2))
    hda_node.parm("shot_index").set(0)  # Ensure we're on the first shot
    hda_node.parm("total").set(1)

def get_shots(hda_node):
    """Retrieves the list of shots from the stored JSON string."""
    data = hda_node.parm("shot_data").eval()

    if not data.strip():  # Prevents json.loads("") from crashing
        init(hda_node)
        data = hda_node.parm("shot_data").eval()  # Re-fetch updated data

    return json.loads(data)

def set_shots(hda_node, shots):
    """Stores the current list of shots into the HDA."""
    hda_node.parm("shot_data").set(json.dumps(shots, indent=2))
    hda_node.parm("total").set(len(shots))

def sync_ui(hda_node):
    """Updates the UI with the current shot's values."""
    shots = get_shots(hda_node)
    shot_index = hda_node.parm("shot_index").eval()

    # Prevent out-of-range index
    if shot_index >= len(shots):
        shot_index = len(shots) - 1
        hda_node.parm("shot_index").set(shot_index)

    current_shot = shots[shot_index] if shots else {}

    # List of parameters to sync
    params_to_sync = [
        "shot_number", "shot_description", "primary_action", "secondary_action", "dialogue",
        "acting_notes", "additional_notes", "audio_notes", "add_image", "use_img_as_background",
        "image_opacity", "image_type", "image_dir", "snapshot_dir", "image_translatex",
        "image_translatey", "image_scalex", "image_scaley", "add_title_screen"
    ]

    for param in params_to_sync:
        value = current_shot.get(param, "")

        # Check if the parameter is numeric before setting
        parm_obj = hda_node.parm(param)
        if parm_obj.parmTemplate().type() in (hou.parmTemplateType.Int, hou.parmTemplateType.Float):
            try:
                parm_obj.set(float(value) if value else 0.0)  # Default to 0 if empty
            except ValueError:
                parm_obj.set(0.0)  # Fallback in case of unexpected errors
        else:
            parm_obj.set(value)

    hda_node.parm("total").set(len(shots))

    
def add_shot(hda_node):
    """Adds a new blank shot and updates the UI."""
    shots = get_shots(hda_node)
    new_shot = {
        "shot_number": "",
        "shot_description": "",
        "primary_action": "",
        "secondary_action": "",
        "dialogue": "",
        "acting_notes": "",
        "additional_notes": "",
        "audio_notes": "",
        "add_image": 0,
        "use_img_as_background": 0,
        "image_opacity": 0.06,
        "image_type": 0,
        "image_dir": "",
        "snapshot_dir": "",
        "image_translatex": -0.5,
        "image_translatey": -0.45,
        "image_scalex": 0.43,
        "image_scaley": 0.43,
        "add_title_screen": 0,
        "image_dir": "opdef:.?imageexample.jpg"
    }
    shots.append(new_shot)
    set_shots(hda_node, shots)

    hda_node.parm("shot_index").set(len(shots) - 1)  # Switch to the new shot
    sync_ui(hda_node)

def remove_shot(hda_node):
    """Removes the current shot, ensuring at least one remains."""
    shots = get_shots(hda_node)
    shot_index = hda_node.parm("shot_index").eval()

    if len(shots) > 1:
        shots.pop(shot_index)
        set_shots(hda_node, shots)

        new_index = max(0, shot_index - 1)  # Move index back if needed
        hda_node.parm("shot_index").set(new_index)

    sync_ui(hda_node)

def store_current_shot(hda_node):
    """Saves the current shot's parameter values into the stored JSON list."""
    shots = get_shots(hda_node)
    shot_index = hda_node.parm("shot_index").eval()

    if 0 <= shot_index < len(shots):  # Prevent out-of-range errors
        shots[shot_index] = {
            "shot_number": hda_node.parm("shot_number").eval(),
            "shot_description": hda_node.parm("shot_description").eval(),
            "primary_action": hda_node.parm("primary_action").eval(),
            "secondary_action": hda_node.parm("secondary_action").eval(),
            "dialogue": hda_node.parm("dialogue").eval(),
            "acting_notes": hda_node.parm("acting_notes").eval(),
            "additional_notes": hda_node.parm("additional_notes").eval(),
            "audio_notes": hda_node.parm("audio_notes").eval(),
            "add_image": hda_node.parm("add_image").eval(),
            "use_img_as_background": hda_node.parm("use_img_as_background").eval(),
            "image_opacity": hda_node.parm("image_opacity").eval(),
            "image_type": hda_node.parm("image_type").eval(),
            "image_dir": hda_node.parm("image_dir").eval(),
            "snapshot_dir": hda_node.parm("snapshot_dir").eval(),
            "image_translatex": hda_node.parm("image_translatex").eval(),
            "image_translatey": hda_node.parm("image_translatey").eval(),
            "image_scalex": hda_node.parm("image_scalex").eval(),
            "image_scaley": hda_node.parm("image_scaley").eval(),
            "add_title_screen": hda_node.parm("add_title_screen").eval()
        }

    set_shots(hda_node, shots)

def render_all(hda_node):
    shots = get_shots(hda_node)
    copnet = hda_node.node("Shots")
    rop = copnet.node("rop_export")
    
    for i in range(len(shots)):
        hda_node.parm("shot_index").set(i)
        sync_ui(hda_node)
        store_current_shot(hda_node)
        hou.ui.triggerUpdate()  # UI update before rendering
        rop.render()

def render_current(hda_node):
    copnet = hda_node.node("Shots")
    rop = copnet.node("rop_export")
    hou.ui.triggerUpdate()
    rop.render()
    
def copy_prev_shot(hda_node):
    """Copies the previous shot's data into the current shot."""
    
    shot_index = hda_node.parm("shot_index").eval()
    shots = get_shots(hda_node)

    if shot_index == 0:
        hou.ui.displayMessage("No previous shot exists!", severity=hou.severityType.Warning)
        return

    # Get previous shot data
    prev_shot_data = shots[shot_index - 1].copy()  # Copy previous shot’s data
    
    # Assign it to current shot
    shots[shot_index] = prev_shot_data
    set_shots(hda_node, shots)
    
    sync_ui(hda_node)

    
def copy_from_shot(hda_node):
    """Opens a Houdini list menu to choose which shot to copy into the current shot."""
    
    shots = get_shots(hda_node)
    shot_index = hda_node.parm("shot_index").eval()

    # Generate menu list
    shot_menu = []
    for i, shot in enumerate(shots):
        shot_menu.append(str(i))  # Shot index
        shot_menu.append(f"Shot {i}: {shot.get('shot_description', 'No Description')}")  # Label
    
    # Open Houdini list menu
    selected_index = hou.ui.selectFromList(
        shot_menu[1::2],  # Show only labels
        message="Select a shot to copy from:",
        title="Copy From Shot",
        exclusive=True
    )

    if selected_index:
        source_index = selected_index[0]  # Get selected shot index
        if source_index != shot_index:  # Avoid copying into itself
            _copy_shot_data(hda_node, source_index, shot_index)  # Call the actual copy function
        else:
            hou.ui.displayMessage("Cannot copy from the same shot!", severity=hou.severityType.Warning)
    

def _copy_shot_data(hda_node, source_index, target_index):
    """Copies data from the selected shot into the current shot."""
    shots = get_shots(hda_node)

    if 0 <= source_index < len(shots) and 0 <= target_index < len(shots):
        shots[target_index] = shots[source_index].copy()  # Copy the selected shot’s data
        set_shots(hda_node, shots)

        # Sync UI to reflect the copied values
        sync_ui(hda_node)

# testing onetwo