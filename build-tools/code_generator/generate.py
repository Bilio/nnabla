# Copyright (c) 2017 Sony Corporation. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import io
import os
from os.path import abspath, dirname, join

here = abspath(dirname(abspath(__file__)))
base = abspath(join(here, '../..'))

import code_generator_utils as utils


def generate_cpp_utils(function_info):
    function_list = utils.info_to_list(function_info)
    utils.generate_from_template(
        join(base, 'src/nbla_utils/nnp_impl_create_function.cpp.tmpl'), function_info=function_info, function_list=function_list)


def generate_proto(function_info, solver_info):
    utils.generate_from_template(
        join(base, 'src/nbla/proto/nnabla.proto.tmpl'), function_info=function_info, solver_info=solver_info)


def generate_python_utils(function_info):
    utils.generate_from_template(
        join(base, 'python/src/nnabla/utils/load_function.py.tmpl'), function_info=function_info)
    utils.generate_from_template(
        join(base, 'python/src/nnabla/utils/save_function.py.tmpl'), function_info=function_info)


def generate_function_python_intereface(function_info):
    utils.generate_from_template(
        join(base, 'python/src/nnabla/function.pyx.tmpl'), function_info=function_info)
    utils.generate_from_template(
        join(base, 'python/src/nnabla/function.pxd.tmpl'), function_info=function_info)
    utils.generate_from_template(
        join(base, 'python/src/nnabla/function_bases.py.tmpl'), function_info=function_info)


def generate_solver_python_intereface(solver_info):
    utils.generate_from_template(
        join(base, 'python/src/nnabla/solver.pyx.tmpl'), solver_info=solver_info)
    utils.generate_from_template(
        join(base, 'python/src/nnabla/solver.pxd.tmpl'), solver_info=solver_info)


def generate():
    function_info = utils.load_function_info(flatten=True)
    solver_info = utils.load_solver_info()
    function_types = utils.load_yaml_ordered(open(
        join(here, 'function_types.yaml'), 'r'))
    solver_types = utils.load_yaml_ordered(open(
        join(here, 'solver_types.yaml'), 'r'))
    utils.generate_init(function_info, function_types,
                        solver_info, solver_types)
    utils.generate_function_types(function_info, function_types)
    utils.generate_solver_types(solver_info, solver_types)
    utils.generate_version()
    generate_solver_python_intereface(solver_info)
    generate_function_python_intereface(function_info)
    generate_python_utils(function_info)
    generate_proto(function_info, solver_info)
    generate_cpp_utils(function_info)

    # Generate function skeltons if new ones are added to functions.yaml and function_types.yaml.
    utils.generate_skelton_function_impl(
        function_info, function_types)
    func_header_template = join(
        base,
        'include/nbla/function/function_impl.hpp.tmpl')
    utils.generate_skelton_function_impl(
        function_info, function_types,
        template=func_header_template, output_format='%s.hpp')

    # TODO: solver skelton generation


if __name__ == '__main__':
    generate()
