"""
MidiAugmenter helper class file
Author: Alex Bourque
"""

from mido import MidiFile, MidiTrack, bpm2tempo, tempo2bpm
import copy
import random

"""
You can use this before you encode and it'll add the augmented midis to the set.
The augmented set it returned, it does not change anything in-place
"""

""" Example: 
midi_set = MidiAugmenter.randomly_augment_set(
  midis=midi_list, 
  augment_chance=0.7, 
  ranges={'pitch':[-4,-2,0,2,4], 'bpm':[-10,0,10]}, 
  shuffle=True
)
"""

class MidiAugmenter(object):
  def randomly_augment_set(midis, augment_chance, ranges, shuffle=True):
    augmented_midis = []
    for midi in midis:
      if random.random() > augment_chance:
        continue
      augmented_midis.append(MidiAugmenter.randomly_augment(midi, ranges))
    augmented_midis += midis
    if shuffle:
      random.shuffle(augmented_midis)
    return augmented_midis

  def randomly_augment(midi, ranges):
    new_midi=copy.deepcopy(midi)
    for k,v in ranges.items():
      new_midi = getattr(MidiAugmenter, 'randomly_augment_'+k)(midi, v)
    return new_midi

  def randomly_augment_pitch(midi, pitch_shift_list):
    pitch_shift = random.choice(pitch_shift_list)
    return MidiAugmenter.augment_pitch(midi, pitch_shift)

  def augment_pitch(midi, pitch_shift):
    print('ps', pitch_shift)
    new_midi = MidiFile()
    for track in midi.tracks:
      new_track = MidiTrack()
      new_midi.tracks.append(new_track)
      for msg in track:
        if msg.is_meta:
          new_track.append(msg.copy())
        else:
          new_track.append(msg.copy(note=max(0, min(127, msg.note+pitch_shift)) ))
    return new_midi

  def randomly_augment_bpm(midi, bpm_shift_list):
    bpm_shift = random.choice(bpm_shift_list)
    return MidiAugmenter.augment_bpm(midi, bpm_shift)

  def augment_bpm(midi, bpm_shift):
    print('bpm', bpm_shift)
    new_midi = copy.deepcopy(midi)
    for track in new_midi.tracks:
      for i, msg in enumerate(track):
        if msg.type == "set_tempo":
          track[i] = msg.copy(tempo=bpm2tempo( tempo2bpm(msg.tempo)+bpm_shift ) )
          break
    return new_midi

  def randomly_augment_tempo(midi, tempo_shift_list):
    tempo_shift = random.choice(tempo_shift_list)
    return MidiAugmenter.augment_tempo(midi, tempo_shift)

  def augment_tempo(midi, tempo_shift):
    print('tempo', tempo_shift)
    new_midi = copy.deepcopy(midi)
    for track in new_midi.tracks:
      for i, msg in enumerate(track):
        if msg.type == "set_tempo":
          track[i] = msg.copy(tempo=msg.tempo+tempo_shift)
          break
    return new_midi
