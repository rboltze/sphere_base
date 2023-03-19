# -*- coding: utf-8 -*-

"""
Sphere shader module. This module contains the Sphere shader class which inherits from the base shader class.
It is used to render Sphere

"""

from OpenGL.GL import *
from OpenGL.GLU import *
from sphere_base.shader.uv_base_shader import BaseShader

from sphere_base.sphere_universe_base.suv_constants import *


class SphereShader(BaseShader):
    def _init_locations(self):
        """
        Initiates the OpenGL locations

        """
        super()._init_locations()
        self.light_id = glGetUniformLocation(self.shader_id, "LightPosition_world_space")
        self.switcher_loc = glGetUniformLocation(self.shader_id, "switcher")

    def set_buffer_bits(self):
        super().set_buffer_bits()

    def draw(self, object_index=0, object_type="", mesh_index=0, indices=None,
             vertices=None, position=None, orientation=None, scale=None, texture_id=0, texture_file="",
             color=None, switch=0):

        super().draw(object_index=object_index, object_type=object_type, mesh_index=mesh_index, indices=indices,
                     vertices=vertices, position=position, orientation=orientation, scale=scale, texture_id=texture_id,
                     texture_file=texture_file, color=color, switch=switch)

        # switch between shaders per object_type
        switch = SHADER_SWITCH[object_type]
        glUniform1i(self.switcher_loc, switch)

        # Using element arrays
        glDrawElements(GL_TRIANGLES, len(indices) * 3, GL_UNSIGNED_INT, ctypes.c_void_p(0))

        # alternative possibility drawing arrays.....
        # glDrawArrays(GL_TRIANGLES, 0, len(vertices))

        glStencilFunc(GL_ALWAYS, object_index, -1)

