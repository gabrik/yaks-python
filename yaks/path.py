# Copyright (c) 2018 ADLINK Technology Inc.
#
# See the NOTICE file(s) distributed with this work for additional
# information regarding copyright ownership.
#
# This program and the accompanying materials are made available under the
# terms of the Eclipse Public License 2.0 which is available at
# http://www.eclipse.org/legal/epl-2.0, or the Apache License, Version 2.0
# which is available at https://www.apache.org/licenses/LICENSE-2.0.
#
# SPDX-License-Identifier: EPL-2.0 OR Apache-2.0
#
# Contributors: Gabriele Baldoni, ADLINK Technology Inc. - Yaks API

import re
from yaks.exceptions import ValidationError


class Path(object):
    def __init__(self, path):
        self.__path_regex = re.compile('^[^?#*]+$')
        if not self.is_valid(path):
            raise ValidationError("{} is not a valid Path".format(path))
        self.path = path

    @staticmethod
    def to_path(p):
        if isinstance(p, Path):
            return p
        else:
            return Path(p)

    def is_valid(self, path):
        return self.__path_regex.match(path) is not None \
            and not path.startswith('//')

    def is_absolute(self):
        if self.path.startswith('/'):
            return True
        return False

    def is_prefix(self, prefix):
        return self.path.startswith(prefix)

    def remove_prefix(self, prefix):
        if self.is_prefix(prefix):
            self.path = self.path[len(prefix):]

    def to_string(self):
        return self.path

    def __len__(self):
        return len(self.path)

    def __eq__(self, second_path):
        if isinstance(second_path, self.__class__):
            return self.path == second_path.path
        return False

    def __str__(self):
        return self.path

    def __repr__(self):
        return self.__str__()

    def __hash__(self):
        return self.path.__hash__()
