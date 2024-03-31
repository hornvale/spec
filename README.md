# _Hornvale_::Specification

A semi-formal specification of Hornvale.

Rather than getting bogged down in implementation details immediately, I want to declare this idea [^1] in some kind of coherent, unambiguous fashion. You know, so I can just _write_ what I want instead of having to specify ownership semantics.

## World

The Game World can be modeled as a directed graph **_G_ = (_V_, _E_)** where:

- _V_ is a set of vertices, with each vertex _v_ ∈ _V_ representing a chunk (node) in the game.
- _E_ is a set of edges, with each edge _e_ ∈ _E_ representing a passage (edge) between chunks. An edge is an ordered pair (_v_<sub>_i_</sub>, _v_<sub>_j_</sub>) indicating a passage from chunk _v_<sub>_i_</sub> to _v_<sub>_j_</sub>.

[^1]:  "You can't just say that your game exists."
  "I didn't say it. I _declared_ it."
