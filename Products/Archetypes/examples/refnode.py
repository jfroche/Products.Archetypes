# -*- coding: UTF-8 -*-
################################################################################
#
# Copyright (c) 2002-2005, Benjamin Saller <bcsaller@ideasuite.com>, and
#                              the respective authors. All rights reserved.
# For a list of Archetypes contributors see docs/CREDITS.txt.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
# * Neither the name of the author nor the names of its contributors may be used
#   to endorse or promote products derived from this software without specific
#   prior written permission.
#
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
################################################################################

from Products.Archetypes.atapi import *
from Products.Archetypes.config import PKG_NAME

schema = BaseSchema + Schema((
    ReferenceField('link',
                   relationship="A",
                   ),

    ReferenceField('links',
                   multiValued=1,
                   relationship="B"
                   ),

    ReferenceField('adds',
                   widget=ReferenceWidget(addable=1),
                   allowed_types=('Refnode', ),
                   relationship="C",
                   multiValued=1,
                   required=1,
                   ),

    ))


class Refnode(BaseContent):
    """A simple archetype for testing references. It can point to itself"""
    schema = schema

registerType(Refnode, PKG_NAME)
