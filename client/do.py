Copyright (c) 2016 Lakshay Piplani

This file is part of YourMessenger.

YourMessenger is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

YourMessenger is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with YourMessenger.  If not, see <http://www.gnu.org/licenses/>.

import cPickle
emptyTxt = ['hey', 'hello how are you', 'fine thank you', 'multilevel marketing', 'multilevel marketing', 'free prize money', 'win free prize', 'multilevel marketing']
emptyLabl = [0, 0, 0, 1, 1, 1, 1, 1]
f = open("clientTxt.pkl", "w")
cPickle.dump(emptyTxt, f)
f.close()
f = open("clientLab.pkl", "w")
cPickle.dump(emptyLabl, f)
f.close()