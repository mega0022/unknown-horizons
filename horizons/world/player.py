# ###################################################
# Copyright (C) 2009 The Unknown Horizons Team
# team@unknown-horizons.org
# This file is part of Unknown Horizons.
#
# Unknown Horizons is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the
# Free Software Foundation, Inc.,
# 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
# ###################################################

from storage import PositiveStorage
from horizons.util import WorldObject, Color
import horizons.main

class Player(WorldObject):
	"""Class representing a player"""

	def __init__(self, id, name, color):
		"""
		@param id: unique player id
		@param name: user-chosen name
		@param color: color of player (as Color)
		"""
		self._init(id, name, color)

		# give a new player 20k coins
		self.inventory.alter(1, 20000)

	def _init(self, id, name, color):
		self.id = id
		self.name = name
		self.color = color
		assert hasattr(self.color, "id"), "Player color has to be a default color"

		self.setup_inventory()

	def setup_inventory(self):
		self.inventory = PositiveStorage()

	def save(self, db):
		client_id = None if self is not horizons.main.session.world.player \
							else horizons.main.settings.client_id
		db("INSERT INTO player(rowid, name, color, client_id) VALUES(?, ?, ?, ?)", \
			 self.getId(), self.name, self.color.id, client_id)
		self.inventory.save(db, self.getId())

	@classmethod
	def load(cls, db, worldid):
		self = Player.__new__(Player)
		self._load(db, worldid)
		return self

	def _load(self, db, worldid):
		"""This function makes it possible to load playerdata into an already allocated
		Player instance, which is used e.g. in Trader.load"""
		super(Player, self).load(db, worldid)

		color, name = db("SELECT color, name FROM player WHERE rowid = ?", worldid)[0]
		self._init(worldid, name, Color[color])

		self.inventory.load(db, worldid)
