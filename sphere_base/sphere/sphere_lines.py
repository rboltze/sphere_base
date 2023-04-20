# -*- coding: utf-8 -*-

from sphere_base.constants import *
from sphere_base.model.model import Model
from sphere_base.utils import dump_exception
from sphere_base.serializable import Serializable
from pyrr import quaternion, vector, Vector3
import numpy as np
import math


class SphereLines(Serializable):
    """
    A class to put longitude and altitude lines on a sphere
    """
    def __init__(self, target_sphere, longitud=15, latitude=15, start_degree=0, color=None, width=1):
        super().__init__('sphere_lines')
        self.sphere = target_sphere
        self.calc = self.sphere.calc
        self.config = self.sphere.config
        self.uv = self.sphere.uv
        self.orientation = self.sphere.orientation
        self.scale = [1.0, 1.0, 1.0]
        self.model = self.set_up_model('sphere_lines')

        self.mesh = self.model.meshes[0]
        self.mesh_id = self.mesh.mesh_id

        self.xyz, self.pos_orientation_offset = None, None
        self.color = color if color else [0, 0, 0, .5]
        self.width = width if width else 5

        self.radius = self.sphere.radius  # - 0.01
        self.sphere.add_item(self)  # register the edge to the base for rendering
        self.create_lines()

    def set_up_model(self, model_name):
        shader, vertex_shader, fragment_shader, geometry_shader = None, None, None, None

        # get the shaders for the edge
        for _name in MODELS.keys():
            if _name == model_name:
                shader = MODELS[_name]["shader"]
                vertex_shader = MODELS[_name]["vertex_shader"]
                fragment_shader = MODELS[_name]["fragment_shader"]
                geometry_shader = MODELS[_name]["geometry_shader"]
                geometry_shader = None if geometry_shader == "none" else geometry_shader

        # create a model for the edge
        model = Model(
                      models=self.uv.models,
                      model_id=0,
                      model_name=model_name,
                      obj_file="",
                      shader=shader,
                      vertex_shader=vertex_shader,
                      fragment_shader=fragment_shader,
                      geometry_shader=geometry_shader)

        return model

    def update_position(self):
        """º
        Recreate the edge when any of the sockets positions change

        """
        # sphere rotates - just update the rotation
        self.orientation = self.sphere.orientation

    def create_lines(self):

        # create an edge for the first time or recreate it during dragging
        pass
        r = self.sphere.radius
        pi = math.pi

        count=1

        vertices = []  # vertex coordinates
        buffer = []
        indices = []
        tex = [1.0, 1.0]  # made up surface edge, that needs to be added to the buffer

        # longitude
        for i in range(0, 360, 15):
            theta = i * (pi / 180.0)
            for j in range(0, 180, 5):
                phi = j * (pi / 180.0)
                x = r * math.sin(phi) * math.cos(theta)
                z = r * math.sin(phi) * math.sin(theta)
                y = r * math.cos(phi)

                p = Vector3([x, y, z])
                n = vector.normalize(Vector3(p) - Vector3(self.sphere.xyz))
                vertices, buffer, indices = self.expand_mesh(vertices, buffer, indices, p, tex, n, count)
                count += 1

        # latitude
        for i in range(0, 360, 15):
            phi = i * (pi / 180.0)
            for j in range(0, 185, 5):
                theta = j * (pi / 180.0)
                x = r * math.sin(phi) * math.cos(theta)
                z = r * math.sin(phi) * math.sin(theta)
                y = r * math.cos(phi)

                p = Vector3([x, y, z])
                n = vector.normalize(Vector3(p) - Vector3(self.sphere.xyz))
                vertices, buffer, indices = self.expand_mesh(vertices, buffer, indices, p, tex, n, count)
                count += 1

        self.mesh.vertices = np.array(vertices, dtype=np.float32)
        self.mesh.indices = np.array(indices, dtype='uint32')
        self.mesh.buffer = np.array(buffer, dtype=np.float32)
        self.mesh.indices_len = len(indices)

        self.xyz = self.sphere.xyz
        self.model.loader.load_mesh_into_opengl(self.mesh_id, self.mesh.buffer,
                                                self.mesh.indices, self.model.shader)

    def expand_mesh(self, vertices, buffer, indices, point, texture, normals, i):
        # This can be used to expanding each point into a mesh.
        p = point
        vertices.extend(p)  # extending the vertices list with the vertex
        buffer = self.extend_buffer(buffer, point, texture, normals)
        indices.append(i)
        return vertices, buffer, indices

    @staticmethod
    def extend_buffer(buffer, vertex, texture, normal):
        buffer.extend(vertex)  # extending the buffer with the vertex
        buffer.extend(texture)  # extending the buffer with the texture
        buffer.extend(normal)  # extending the buffer with the normal
        return buffer

    def remove(self):
        pass

    def draw(self):
        """
        Renders the edge.
        """

        try:
            self.model.draw(self, color=self.color)

        except Exception as e:
            dump_exception(e)