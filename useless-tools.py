# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth reFloor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

bl_info = {
    "name": "Useless Tools",
    "description": "Just a little collection of scripts and tools I use daily",
    "author": "Greg Zaal",
    "version": (1, 2),
    "blender": (2, 75, 0),
    "location": "Mostly 3D view toolshelf",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "System"}


import bpy
import os

global obtypes
obtypes = ['MESH', 'CURVE', 'SURFACE', 'META', 'FONT', 'ARMATURE', 'LATTICE', 'EMPTY', 'CAMERA', 'LAMP']


class UTSetSelectable(bpy.types.Operator):

    'Sets selectability for the selected objects'
    bl_idname = 'ut.set_selectable'
    bl_label = 'set selectable'
    selectable = bpy.props.BoolProperty()

    def execute(self, context,):
        for obj in bpy.context.selected_objects:
            if self.selectable == True:
                obj.hide_select = False
            else:
                obj.hide_select = True
        return {'FINISHED'}


class UTSetRenderable(bpy.types.Operator):

    'Sets renderability for the selected objects'
    bl_idname = 'ut.set_renderable'
    bl_label = 'set renderable'
    renderable = bpy.props.BoolProperty()

    def execute(self, context,):
        for obj in bpy.context.selected_objects:
            if self.renderable == True:
                obj.hide_render = False
            else:
                obj.hide_render = True
        return {'FINISHED'}


class UTAllSelectable(bpy.types.Operator):

    'Allows all objects to be selected'
    bl_idname = 'ut.all_selectable'
    bl_label = 'all selectable'

    def execute(self, context,):
        for obj in bpy.data.objects:
            obj.hide_select = False
        return {'FINISHED'}


class UTAllRenderable(bpy.types.Operator):

    'Allows all objects to be rendered'
    bl_idname = 'ut.all_renderable'
    bl_label = 'all renderable'

    def execute(self, context,):
        for obj in bpy.data.objects:
            obj.hide_render = False
        return {'FINISHED'}


class UTSelNGon(bpy.types.Operator):

    'Selects faces with more than 4 vertices'
    bl_idname = 'ut.select_ngons'
    bl_label = 'Select NGons'

    @classmethod
    def poll(cls, context):
        if not context.active_object or context.mode != 'EDIT_MESH':
            return False
        else:
            return True

    def execute(self, context):
        context.tool_settings.mesh_select_mode = (False, False, True)
        bpy.ops.mesh.select_face_by_sides(number=4, type='GREATER', extend=True)
        return {'FINISHED'}


class UTWireHideSel(bpy.types.Operator):

    'Hides the wire overlay of all objects in the selection'
    bl_idname = 'ut.wirehidesel'
    bl_label = 'Hide Wire'
    show = bpy.props.BoolProperty(default=False)

    def execute(self, context):
        for e in bpy.context.selected_objects:
            try:
                e.show_wire = self.show
            except KeyError:
                print("Error on " + e.name)
        return {'FINISHED'}


class UTWireHideAll(bpy.types.Operator):

    'Hides the wire overlay of all objects'
    bl_idname = 'ut.wirehideall'
    bl_label = 'Hide Wire (All)'
    show = bpy.props.BoolProperty(default=False)

    def execute(self, context):
        for e in bpy.data.objects:
            try:
                e.show_wire = self.show
            except KeyError:
                print("Error on " + e.name)
        return {'FINISHED'}


class UTSubsurfHideSel(bpy.types.Operator):

    'Sets the Subsurf modifier of all objects in selection to be invisible in the viewport'
    bl_idname = 'ut.subsurfhidesel'
    bl_label = 'Subsurf Hide'
    show = bpy.props.BoolProperty(default=False)

    def execute(self, context):
        for e in bpy.context.selected_objects:
            try:
                e.modifiers['Subsurf'].show_viewport = self.show
            except KeyError:
                print("No subsurf on " + e.name + " or it is not named Subsurf")
        return {'FINISHED'}


class UTSubsurfHideAll(bpy.types.Operator):

    'Sets the Subsurf modifier of all objects to be invisible in the viewport'
    bl_idname = 'ut.subsurfhideall'
    bl_label = 'Subsurf Hide (All)'
    show = bpy.props.BoolProperty(default=False)

    def execute(self, context):
        for e in bpy.data.objects:
            try:
                e.modifiers['Subsurf'].show_viewport = self.show
            except KeyError:
                print("No subsurf on " + e.name + " or it is not named Subsurf")
        return {'FINISHED'}


class UTOptimalDisplaySel(bpy.types.Operator):

    'Disables Optimal Display for all Subsurf modifiers on selected objects'
    bl_idname = 'ut.optimaldisplaysel'
    bl_label = 'Optimal Display'
    on = bpy.props.BoolProperty(default=False)

    def execute(self, context):
        for o in bpy.context.selected_objects:
            for m in o.modifiers:
                if m.type in ['SUBSURF', 'MULTIRES']:
                    m.show_only_control_edges = self.on
        return {'FINISHED'}


class UTOptimalDisplayAll(bpy.types.Operator):

    'Disables Optimal Display for all Subsurf modifiers'
    bl_idname = 'ut.optimaldisplayall'
    bl_label = 'Optimal Display Off (All)'
    on = bpy.props.BoolProperty(default=False)

    def execute(self, context):
        for o in bpy.data.objects:
            for m in o.modifiers:
                if m.type in ['SUBSURF', 'MULTIRES']:
                    m.show_only_control_edges = self.on
        return {'FINISHED'}


class UTAllEdges(bpy.types.Operator):

    'Enables All Edges for all objects'
    bl_idname = 'ut.all_edges'
    bl_label = 'All Edges'
    on = bpy.props.BoolProperty(default=False)

    def execute(self, context):
        for e in bpy.data.objects:
            e.show_all_edges = self.on
        return {'FINISHED'}


class UTDoubleSided(bpy.types.Operator):

    'Disables Double Sided Normals for all objects'
    bl_idname = 'ut.double_sided'
    bl_label = 'Double Sided Normals'
    on = bpy.props.BoolProperty(default=False)

    def execute(self, context):
        for e in bpy.data.meshes:
            try:
                e.show_double_sided = self.on
            except KeyError:
                print("Error setting double sided on " + e.name)
        return {'FINISHED'}


class UTClearAnim(bpy.types.Operator):

    'Deletes animation for the selected objects'
    bl_idname = 'ut.clearanim'
    bl_label = 'Delete Animation'
    selected_only = bpy.props.BoolProperty(default=False)

    def execute(self, context):
        if self.selected_only:
            objs = bpy.context.selected_objects
        else:
            objs = bpy.data.objects

        for obj in objs:
            obj.animation_data_clear()

        self.report({'INFO'}, "Animation deleted")
        return {'FINISHED'}


class UTKillSubsurfs(bpy.types.Operator):

    'Deletes all Subsurf modifiers in the scene'
    bl_idname = 'ut.remove_all_subsurfs'
    bl_label = 'Kill All Subsurfs'

    def execute(self, context,):
        counter = 0
        for obj in bpy.data.objects:
            bpy.context.scene.objects.active = obj
            for mod in bpy.context.object.modifiers:
                if mod.type == 'SUBSURF':
                    if context.mode == "EDIT_MESH":
                        bpy.ops.object.editmode_toggle()
                        bpy.ops.object.modifier_remove(modifier=mod.name)
                        bpy.ops.object.editmode_toggle()
                    else:
                        bpy.ops.object.modifier_remove(modifier=mod.name)
                    counter = counter + 1
        self.report({'INFO'}, str(counter) + " subsurfs removed!")
        return {'FINISHED'}


class UTDrawTypeOp(bpy.types.Operator):

    'Sets draw type for the selected objects'
    bl_idname = 'ut.set_draw_type'
    bl_label = 'Draw Type'
    prop = bpy.props.StringProperty()

    def execute(self, context,):
        for obj in bpy.context.selected_objects:
            obj.draw_type = self.prop
        return {'FINISHED'}


class UTDrawTypeMenu(bpy.types.Menu):
    bl_idname = 'OBJECT_MT_DrawTypeMenu'
    bl_label = "Draw Type"

    def draw(self, context):
        layout = self.layout
        layout.operator("ut.set_draw_type", text="Textured").prop = "TEXTURED"
        layout.operator("ut.set_draw_type", text="Solid").prop = "SOLID"
        layout.operator("ut.set_draw_type", text="Wire").prop = "WIRE"
        layout.operator("ut.set_draw_type", text="Bounds").prop = "BOUNDS"


class UTSetLens(bpy.types.Operator):

    'Sets viewport lense to 100mm'
    bl_idname = 'ut.set_lens'
    bl_label = 'Set Lens'
    prop = bpy.props.IntProperty(default = 35)

    def execute(self, context,):
        bpy.context.space_data.lens = self.prop
        return {'FINISHED'}


class UTOriginToSel(bpy.types.Operator):

    'Moves object origin to selection (Edit mode only, cannot undo)'
    bl_idname = 'ut.origin_to_selected'
    bl_label = 'Origin to Selected'

    @classmethod
    def poll(cls, context):
        return context.active_object and (bpy.context.mode == 'EDIT_MESH' or bpy.context.mode == 'EDIT_CURVE')

    def execute(self, context,):
        curloc = bpy.context.scene.cursor_location
        curx = curloc.x
        cury = curloc.y
        curz = curloc.z

        bpy.ops.view3d.snap_cursor_to_selected()
        bpy.ops.object.editmode_toggle()
        bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')
        bpy.ops.object.editmode_toggle()
        bpy.context.scene.cursor_location.x = curx
        bpy.context.scene.cursor_location.y = cury
        bpy.context.scene.cursor_location.z = curz
        return {'FINISHED'}


class UTRecalcNormalsObjects(bpy.types.Operator):

    'Recalculate normals of all selected objects'
    bl_idname = 'ut.recalculate_normals'
    bl_label = 'Recalculate Normals'

    @classmethod
    def poll(cls, context):
        return bpy.context.mode == 'OBJECT' and bpy.context.selected_objects

    def execute(self, context,):
        objs = context.selected_objects
        oldactive = context.active_object

        for obj in objs:
            if obj.type == 'MESH':
                context.scene.objects.active = obj
                bpy.ops.object.editmode_toggle()
                bpy.ops.mesh.select_all(action='SELECT')
                bpy.ops.mesh.normals_make_consistent(inside=False)
                bpy.ops.object.editmode_toggle()
                self.report({'INFO'}, "Recalculated normals of " + obj.name)
        return {'FINISHED'}


class UTSaveFile(bpy.types.Operator):

    'Saves the File, or Save As if not saved already'
    bl_idname = 'ut.save_file'
    bl_label = 'Save File'

    @classmethod
    def poll(cls, context):
        return bpy.data.filepath != "" and not bpy.data.filepath.endswith("untitled.blend")

    def execute(self, context,):
        if bpy.data.filepath != "":
            bpy.ops.wm.save_mainfile(filepath=bpy.data.filepath)
        else:
            bpy.ops.wm.save_as_mainfile()
        return {'FINISHED'}


class UTSaveFileIncrement(bpy.types.Operator):

    'Increments the file name and then saves it'
    bl_idname = 'ut.save_file_increment'
    bl_label = 'Save File Increment'

    @classmethod
    def poll(cls, context):
        return bpy.data.filepath[-7:-6].isnumeric()

    def execute(self, context,):
        if bpy.data.filepath != "":
            fp = bpy.data.filepath
            enddigit = fp[-7:-6]
            end2digit = fp[-8:-7]
            end3digit = fp[-9:-8]
            if enddigit.isnumeric():
                if int(enddigit) == 9 and not end2digit.isnumeric():
                    endint = int(enddigit) + 1
                    fp = fp[:-7] + str(endint) + fp[-6:]
                if int(enddigit) != 9:
                    endint = int(enddigit) + 1
                    fp = fp[:-7] + str(endint) + fp[-6:]
                if end2digit.isnumeric() and int(enddigit) == 9:
                    endint = 0
                    end2int = int(end2digit) + 1
                    fp = fp[:-8] + str(end2int) + str(endint) + fp[-6:]
                if end3digit.isnumeric() and int(end2digit) == 9 and int(enddigit) == 9:
                    endint = 0
                    end2int = 0
                    end3int = int(end3digit) + 1
                    fp = fp[:-10] + str(end3int) + str(end2int) + str(endint) + fp[-6:]
            splitsep = fp.split(os.sep)
            self.report({'INFO'}, "Saved as " + splitsep[len(splitsep) - 1])
            bpy.ops.wm.save_as_mainfile(filepath=fp)
        else:
            print("saving as...")
            bpy.ops.wm.save_as_mainfile()
        return {'FINISHED'}


class UTClippingToggle(bpy.types.Operator):

    'Toggles mirror modifiers clipping property'
    bl_idname = 'ut.mirror_clipping'
    bl_label = 'Toggle Clipping'

    @classmethod
    def poll(cls, context):
        hasmirror = False
        for obj in bpy.context.selected_objects:
            for mod in obj.modifiers:
                if mod.type == 'MIRROR':
                    hasmirror = True
        return hasmirror

    def execute(self, context):
        for e in bpy.context.selected_objects:
            try:
                if e.modifiers['Mirror'].use_clip == True:
                    e.modifiers['Mirror'].use_clip = False
                elif e.modifiers['Mirror'].use_clip == False:
                    e.modifiers['Mirror'].use_clip = True
            except KeyError:
                print("No mirror modifier on " + e.name + " or it is not named Mirror")
        return {'FINISHED'}
    
    
class UTEmptyAlign(bpy.types.Operator):

    'Sets the offset of the image'
    bl_idname = 'ut.align_empty'
    bl_label = 'Align'
    pos = bpy.props.StringProperty()

    @classmethod
    def poll(cls, context):
        isimage = False
        if context.active_object.empty_draw_type == 'IMAGE':
            isimage = True
        return isimage

    def execute(self, context,):
        pos = self.pos
        px = 0
        py = 0

        if pos == "U_L":
            px = 0
            py = -1
        if pos == "U_M":
            px = -0.5
            py = -1
        if pos == "U_R":
            px = -1
            py = -1
        if pos == "M_L":
            px = 0
            py = -0.5
        if pos == "M_M":
            px = -0.5
            py = -0.5
        if pos == "M_R":
            px = -1
            py = -0.5
        if pos == "D_L":
            px = 0
            py = 0
        if pos == "D_M":
            px = -0.5
            py = 0
        if pos == "D_R":
            px = -1
            py = 0

        obj = bpy.context.active_object
        if not context.scene.UTEmptySlide:
            obj.empty_image_offset[0] = px
            obj.empty_image_offset[1] = py
        else:
            dx = obj.empty_image_offset[0] - px
            dy = obj.empty_image_offset[1] - py
            obj.empty_image_offset[0] = px
            obj.empty_image_offset[1] = py
            obj.location.x = obj.location.x + (dx * obj.empty_draw_size * obj.scale.x)
            obj.location.y = obj.location.y + (dy * obj.empty_draw_size * obj.scale.y)

            goodrot = True
            if obj.rotation_euler.x != 0 or obj.rotation_euler.y != 0 or obj.rotation_euler.z != 0 or obj.rotation_quaternion.w != 1 or obj.rotation_quaternion.x != 0 or obj.rotation_quaternion.y != 0 or obj.rotation_quaternion.z != 0 or obj.rotation_axis_angle[0] != 0 or obj.rotation_axis_angle[1] != 0 or obj.rotation_axis_angle[2] != 1 or obj.rotation_axis_angle[3] != 0:
                goodrot = False
            if goodrot == False and context.scene.UTEmptySlide == True:
                self.report({'WARNING'}, "CAUTION! Aligning images with 'Slide Origin' on and a non-default rotation may have unexpected results")
        return {'FINISHED'}


class UTAddPositionedSuzanne(bpy.types.Operator):

    'Add a monkey that sits on the ground'
    bl_idname = 'ut.positioned_suz'
    bl_label = 'Positioned Suzanne'

    @classmethod
    def poll(cls, context):
        return (context.mode == 'OBJECT')

    def execute(self, context):
        cloc = context.scene.cursor_location
        bpy.ops.mesh.primitive_monkey_add(radius=1, view_align=False, enter_editmode=False, location=(cloc.x, cloc.y, cloc.z+0.4955), layers=(True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False))
        bpy.ops.object.shade_smooth()
        bpy.ops.object.subdivision_set(level=3)
        bpy.context.object.modifiers["Subsurf"].render_levels = 3
        bpy.context.object.rotation_euler.x = -0.6254132986068726

        return {'FINISHED'}


class UTDeleteNodeGroups(bpy.types.Operator):

    'Disables Fake User and reloads the file. Click this several times until there are no unused groups left'
    bl_idname = 'ut.delete_node_groups'
    bl_label = 'Delete Unused Node Groups'

    @classmethod
    def poll(cls, context):
        return bpy.data.filepath != "" and not bpy.data.filepath.endswith("untitled.blend")

    def execute(self, context):
        groups = bpy.data.node_groups

        num_groups = len(groups)
        num_affected = 0
        for g in groups:
            if g.use_fake_user:
                g.use_fake_user = False
                num_affected += 1

        bpy.ops.wm.save_reload()

        self.report({'INFO'}, ("Affected " + str(num_affected) + " of " + str(num_groups)))

        return {'FINISHED'}


class UTCameraBroder(bpy.types.Operator):

    'Use the whole camera field of view as border, to speed up viewport rendering'
    bl_idname = 'ut.cam_border'
    bl_label = 'Use Camera as Border'

    def execute(self, context,):
        r = context.scene.render
        r.use_border = True
        r.border_min_x = 0
        r.border_min_y = 0
        r.border_max_x = 1
        r.border_max_y = 1

        return {'FINISHED'}


def menu_func_objspecials(self, context):
    layout = self.layout
    layout.separator()
    layout.operator("object.shade_smooth", text='Shade Smooth')
    layout.operator("object.shade_flat", text='Shade Flat')
    layout.separator()
    layout.menu("OBJECT_MT_DrawTypeMenu")
    layout.separator()
    layout.operator("ut.cam_border")


def menu_func_origintosel(self, context):
    layout = self.layout

    if context.active_object and (bpy.context.mode == 'EDIT_MESH' or bpy.context.mode == 'EDIT_CURVE'):
        col = layout.column()
        col.separator()
        col.operator("ut.origin_to_selected")


def menu_func_renderres(self, context):
    layout = self.layout

    rend = context.scene.render
    rend_percent = rend.resolution_percentage * 0.01
    x = (str(rend.resolution_x * rend_percent).split('.'))[0]
    y = (str(rend.resolution_y * rend_percent).split('.'))[0]
    layout.label(text="Actual Render Resolution: " + x + " x " + y)


def menu_func_filefuncs(self, context):
    layout = self.layout

    col = layout.column()
    row = col.row(align=True)
    row.alignment = 'CENTER'
    row.operator("ut.save_file", icon="FILE_TICK", text="")
    row.operator("ut.save_file_increment", icon="ZOOMIN", text="")
    row.operator("wm.save_as_mainfile", icon="SAVE_AS", text="")
    row.operator("wm.open_mainfile", icon="FILE_FOLDER", text="")


def menu_func_emptyfuncs(self, context):
    layout = self.layout
    scene = context.scene

    col = layout.column(align=True)
    row = col.row(align=True)
    row.label(text="Align Image:")
    row.prop(scene, "UTEmptySlide")
    col = layout.column(align=True)
    row = col.row(align=True)
    row.alignment = 'CENTER'
    row.operator("ut.align_empty", text="").pos = "U_L"
    row.operator("ut.align_empty", text="").pos = "U_M"
    row.operator("ut.align_empty", text="").pos = "U_R"
    row = col.row(align=True)
    row.alignment = 'CENTER'
    row.operator("ut.align_empty", text="").pos = "M_L"
    row.operator("ut.align_empty", text="").pos = "M_M"
    row.operator("ut.align_empty", text="").pos = "M_R"
    row = col.row(align=True)
    row.alignment = 'CENTER'
    row.operator("ut.align_empty", text="").pos = "D_L"
    row.operator("ut.align_empty", text="").pos = "D_M"
    row.operator("ut.align_empty", text="").pos = "D_R"


def menu_func_3dviewheader(self, context):
    layout = self.layout

    if context.mode != 'SCULPT':
        col = layout.column()
        row = col.row(align=True)
        row.alignment = 'CENTER'
        row.operator("ut.set_selectable", icon="RESTRICT_SELECT_ON", text="").selectable = False
        row.operator("ut.set_selectable", icon="RESTRICT_SELECT_OFF", text="").selectable = True
        row.operator("ut.set_renderable", icon="RESTRICT_RENDER_ON", text="").renderable = False
        row.operator("ut.set_renderable", icon="RESTRICT_RENDER_OFF", text="").renderable = True

        col = layout.column()
        row = col.row(align=True)
        row.operator("ut.all_selectable", icon="RESTRICT_SELECT_OFF", text="")
        row.operator("ut.all_renderable", icon="RESTRICT_RENDER_OFF", text="")
    else:
        col = layout.column()
        row = col.row(align=True)
        row.prop(context.object, 'show_wire')


    col = layout.column()
    row = col.row(align=True)
    row.operator("ut.set_lens", text="35").prop=35
    row.operator("ut.set_lens", text="100").prop=100


def menu_func_addobj(self, context):
    self.layout.operator("ut.positioned_suz", icon="MONKEY")
    
def menu_func_vse(self, context):
    scene = bpy.context.scene
    sequences = scene.sequence_editor.sequences
    frame = scene.frame_current

    shotname = ""
    sequences_at_frame = []
    if sequences:
        for seq in sequences:
            if (seq.frame_start <= frame <= seq.frame_start+seq.frame_duration):
                sequences_at_frame.append(seq)

        if sequences_at_frame:        
            shotname = sorted(sequences_at_frame, key=lambda k: k.channel)[0].name.split('.')[0]
            self.layout.column().row().label("Strip: "+shotname)

class UselessToolsPanel(bpy.types.Panel):
    bl_label = "Useless Tools"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_category = "Addons"

    def draw(self, context):
        scene = context.scene
        SUBSURFDROP = scene.UTSubSurfDrop
        WIREDROP = scene.UTWireDrop
        VIEWPORTDROP = scene.UTViewPortDrop
        MISCDROP = scene.UTMiscDrop
        view = context.space_data
        toolsettings = context.tool_settings
        layout = self.layout

        box1 = self.layout.box()
        col = box1.column(align=True)
        row = col.row(align=True)
        row.prop(scene, "UTSubSurfDrop", icon="TRIA_DOWN")
        if not SUBSURFDROP:
            row.operator("ut.subsurfhideall", icon="MOD_SOLIDIFY", text="").show=False
            row.operator("ut.subsurfhideall", icon="MOD_SUBSURF", text="").show=True
            row.operator("ut.optimaldisplayall", icon="MESH_PLANE", text="").on=True
        if SUBSURFDROP:
            row1 = col.row(align=True)
            row1.operator("ut.subsurfhidesel", icon="MOD_SOLIDIFY", text="Hide").show=False
            row1.operator("ut.subsurfhidesel", icon="MOD_SUBSURF", text="Show").show=True
            row2 = col.row(align=True)
            row2.operator("ut.subsurfhideall", icon="MOD_SOLIDIFY", text="Hide All").show=False
            row2.operator("ut.subsurfhideall", icon="MOD_SUBSURF", text="Show All").show=True
            row3 = col.row(align=True)
            row3.operator("ut.optimaldisplaysel", icon="MESH_GRID", text="S").on=False
            row3.operator("ut.optimaldisplaysel", icon="MESH_PLANE", text="S").on=True
            row3.operator("ut.optimaldisplayall", icon="MESH_GRID", text="A").on=False
            row3.operator("ut.optimaldisplayall", icon="MESH_PLANE", text="A").on=True
            row4 = col.row(align=True)
            row4.operator("ut.remove_all_subsurfs", icon="PANEL_CLOSE")

        box1 = self.layout.box()
        col = box1.column(align=True)
        row = col.row(align=True)
        row.prop(scene, "UTWireDrop", icon="TRIA_DOWN")
        if not WIREDROP:
            row.operator("ut.wirehideall", icon="MATSPHERE", text="").show=False
            row.operator("ut.wirehideall", icon="MESH_UVSPHERE", text="").show=True
            row.operator("ut.all_edges", icon="MESH_GRID", text="").on=True
        if WIREDROP:
            row1 = col.row(align=True)
            row1.operator("ut.wirehidesel", icon="MATSPHERE", text="Hide").show=False
            row1.operator("ut.wirehidesel", icon="MESH_UVSPHERE", text="Show").show=True
            row2 = col.row(align=True)
            row2.operator("ut.wirehideall", icon="MATSPHERE", text="Hide All").show=False
            row2.operator("ut.wirehideall", icon="MESH_UVSPHERE", text="Show All").show=True
            row3 = col.row(align=True)
            row3.alignment = 'CENTER'
            row3.label(text="All Edges:")
            row3.operator("ut.all_edges", icon="MESH_PLANE", text="Off").on=False
            row3.operator("ut.all_edges", icon="MESH_GRID", text="On").on=True

        box1 = self.layout.box()
        col = box1.column(align=True)
        row = col.row(align=True)
        row.prop(scene, "UTViewPortDrop", icon="TRIA_DOWN")
        if not VIEWPORTDROP:
            row.operator("ut.double_sided", icon="CLIPUV_DEHLT", text="").on=False
            row.operator("ut.set_lens", icon="OUTLINER_DATA_CAMERA", text="").prop=35
            row.prop(bpy.context.user_preferences.system, "use_vertex_buffer_objects", text="")
        if VIEWPORTDROP:
            row3 = col.row(align=True)
            row3.alignment = 'CENTER'
            row3.label(text="Sides:")
            row3.operator("ut.double_sided", icon="CLIPUV_HLT", text="2x").on=True
            row3.operator("ut.double_sided", icon="CLIPUV_DEHLT", text="1x").on=False
            row5 = col.row(align=True)
            row5.prop(bpy.context.user_preferences.system, "use_vertex_buffer_objects")
            row5.prop(view, "show_backface_culling")
            col.prop(view, "lens")
            row4 = col.row(align=True)
            row4.operator("ut.set_lens", text="18").prop=18
            row4.operator("ut.set_lens", text="35").prop=35
            row4.operator("ut.set_lens", text="50").prop=50
            row4.operator("ut.set_lens", text="70").prop=70
            row4.operator("ut.set_lens", text="100").prop=100

        box1 = self.layout.box()
        col = box1.column(align=True)
        row = col.row(align=True)
        row.prop(scene, "UTMiscDrop", icon="TRIA_DOWN")
        if not MISCDROP:
            row.operator("ut.recalculate_normals", icon="SNAP_NORMAL", text="")
            row.operator("ut.mirror_clipping", icon="MOD_MIRROR", text="")
            row.operator("ut.select_ngons", icon="MOD_BEVEL", text="")
        if MISCDROP:
            row = col.row(align=True)
            row.alignment = 'CENTER'
            row.label(text="Del Anim")
            row.operator("ut.clearanim", text="Sel").selected_only=True
            row.operator("ut.clearanim", text="All").selected_only=False
            col.separator()
            row = col.row(align=True)
            row.alignment = 'CENTER'
            row.label(text="Mirror Clipping")
            row.operator("ut.mirror_clipping", text="Toggle")
            col.separator()
            col.operator("ut.select_ngons", icon="MOD_BEVEL")
            col.operator("ut.recalculate_normals", icon="SNAP_NORMAL")
            col.separator()
            col.operator("ut.delete_node_groups", icon="CANCEL", text="("+str(len(bpy.data.node_groups))+") Delete Unused Node Groups")


def register():
    bpy.types.Scene.UTSubSurfDrop = bpy.props.BoolProperty(
        name="Subsurf",
        default=False,
        description="Quick batch subsurf control")
    bpy.types.Scene.UTWireDrop = bpy.props.BoolProperty(
        name="Wire",
        default=False,
        description="Wire display and overlay controls")
    bpy.types.Scene.UTViewPortDrop = bpy.props.BoolProperty(
        name="View",
        default=False,
        description="Viewport display and performance tweaks")
    bpy.types.Scene.UTMiscDrop = bpy.props.BoolProperty(
        name="Misc",
        default=False,
        description="I love your robot hand!")
    bpy.types.Scene.UTEmptySlide = bpy.props.BoolProperty(
        name="Slide Origin",
        default=False,
        description="Move object opposite to image offset to keep visual location constant (square images only)")

    bpy.utils.register_module(__name__)
    bpy.types.VIEW3D_MT_object_specials.append(menu_func_objspecials)
    bpy.types.VIEW3D_MT_snap.append(menu_func_origintosel)
    bpy.types.RENDER_PT_dimensions.append(menu_func_renderres)
    bpy.types.INFO_HT_header.prepend(menu_func_filefuncs)
    bpy.types.DATA_PT_empty.append(menu_func_emptyfuncs)
    bpy.types.VIEW3D_HT_header.append(menu_func_3dviewheader)
    bpy.types.INFO_MT_mesh_add.append(menu_func_addobj)
    bpy.types.SEQUENCER_HT_header.append(menu_func_vse)


def unregister():
    del bpy.types.Scene.UTSubSurfDrop
    del bpy.types.Scene.UTWireDrop
    del bpy.types.Scene.UTViewPortDrop
    del bpy.types.Scene.UTMiscDrop
    bpy.utils.unregister_module(__name__)
    bpy.types.VIEW3D_MT_object_specials.remove(menu_func_objspecials)
    bpy.types.VIEW3D_MT_snap.remove(menu_func_origintosel)
    bpy.types.RENDER_PT_dimensions.remove(menu_func_renderres)
    bpy.types.INFO_HT_header.remove(menu_func_filefuncs)
    bpy.types.DATA_PT_empty.remove(menu_func_emptyfuncs)
    bpy.types.VIEW3D_HT_header.remove(menu_func_3dviewheader)
    bpy.types.INFO_MT_mesh_add.remove(menu_func_addobj)
    bpy.types.SEQUENCER_HT_header.remove(menu_func_vse)

if __name__ == "__main__":
    register()
