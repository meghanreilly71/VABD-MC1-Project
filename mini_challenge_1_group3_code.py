import marimo

__generated_with = "0.19.2"
app = marimo.App(width="full")


@app.cell
def _(mo):
    mo.md(r"""
    # MC1 Graph Data — Preparation for Visualisation
    VAST 2025 Mini Challenge 1: Musical influence network (17,412 nodes, 37,857 edges)
    """)
    return


@app.cell
def _():
    import json
    import pandas as pd
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches
    import networkx as nx
    from collections import defaultdict
    import marimo as mo
    import altair as alt
    from collections import Counter
    return Counter, alt, defaultdict, json, mo, mpatches, nx, pd, plt


@app.cell
def _(defaultdict, mpatches, nx, plt):
    # Visualise the graph schema: node types and edge types
    schema = nx.MultiDiGraph()

    node_types = ["Person", "MusicalGroup", "RecordLabel", "Song", "Album"]
    node_colors = {
        "Person": "#4ECDC4",
        "MusicalGroup": "#FF6B6B",
        "RecordLabel": "#FFE66D",
        "Song": "#95E1D3",
        "Album": "#F38181",
    }
    for nt in node_types:
        schema.add_node(nt)

    schema_edges = [
        ("Person", "Song", "PerformerOf"),
        ("Person", "Album", "PerformerOf"),
        ("MusicalGroup", "Song", "PerformerOf"),
        ("MusicalGroup", "Album", "PerformerOf"),
        ("Person", "Song", "ComposerOf"),
        ("Person", "Album", "ComposerOf"),
        ("Person", "Song", "ProducerOf"),
        ("Person", "Album", "ProducerOf"),
        ("Person", "Person", "ProducerOf"),
        ("Person", "MusicalGroup", "ProducerOf"),
        ("RecordLabel", "Song", "ProducerOf"),
        ("RecordLabel", "Album", "ProducerOf"),
        ("Person", "Song", "LyricistOf"),
        ("Person", "Album", "LyricistOf"),
        ("Song", "RecordLabel", "RecordedBy"),
        ("Album", "RecordLabel", "RecordedBy"),
        ("Song", "RecordLabel", "DistributedBy"),
        ("Album", "RecordLabel", "DistributedBy"),
        ("Song", "Song", "InStyleOf"),
        ("Song", "Album", "InStyleOf"),
        ("Song", "Person", "InStyleOf"),
        ("Song", "MusicalGroup", "InStyleOf"),
        ("Album", "Song", "InStyleOf"),
        ("Album", "Album", "InStyleOf"),
        ("Album", "Person", "InStyleOf"),
        ("Album", "MusicalGroup", "InStyleOf"),
        ("Song", "Song", "InterpolatesFrom"),
        ("Song", "Album", "InterpolatesFrom"),
        ("Album", "Song", "InterpolatesFrom"),
        ("Album", "Album", "InterpolatesFrom"),
        ("Song", "Song", "CoverOf"),
        ("Song", "Album", "CoverOf"),
        ("Album", "Song", "CoverOf"),
        ("Album", "Album", "CoverOf"),
        ("Song", "Song", "LyricalReferenceTo"),
        ("Song", "Album", "LyricalReferenceTo"),
        ("Album", "Song", "LyricalReferenceTo"),
        ("Album", "Album", "LyricalReferenceTo"),
        ("Song", "Song", "DirectlySamples"),
        ("Song", "Album", "DirectlySamples"),
        ("Album", "Song", "DirectlySamples"),
        ("Album", "Album", "DirectlySamples"),
        ("Person", "MusicalGroup", "MemberOf"),
    ]

    for src, tgt, etype in schema_edges:
        schema.add_edge(src, tgt, label=etype)

    fig, ax = plt.subplots(figsize=(14, 10))
    pos = {
        "Person": (-1, 1),
        "MusicalGroup": (1, 1),
        "RecordLabel": (0, -1),
        "Song": (-1.5, 0),
        "Album": (1.5, 0),
    }

    for nt in node_types:
        nx.draw_networkx_nodes(
            schema,
            pos,
            nodelist=[nt],
            node_color=node_colors[nt],
            node_size=3000,
            ax=ax,
        )
    nx.draw_networkx_labels(schema, pos, font_size=10, font_weight="bold", ax=ax)

    edge_colors_map = {
        "PerformerOf": "#2196F3",
        "ComposerOf": "#4CAF50",
        "ProducerOf": "#FF9800",
        "LyricistOf": "#9C27B0",
        "RecordedBy": "#795548",
        "DistributedBy": "#607D8B",
        "InStyleOf": "#E91E63",
        "InterpolatesFrom": "#00BCD4",
        "CoverOf": "#F44336",
        "LyricalReferenceTo": "#CDDC39",
        "DirectlySamples": "#FF5722",
        "MemberOf": "#3F51B5",
    }

    edge_groups = defaultdict(list)
    for src, tgt, etype in schema_edges:
        edge_groups[(src, tgt)].append(etype)

    for (src, tgt), etypes in edge_groups.items():
        for i, etype in enumerate(etypes):
            rad = 0.1 + i * 0.15
            nx.draw_networkx_edges(
                schema,
                pos,
                edgelist=[(src, tgt)],
                ax=ax,
                edge_color=edge_colors_map[etype],
                width=1.5,
                connectionstyle=f"arc3,rad={rad}",
                arrows=True,
                arrowsize=15,
                alpha=0.7,
            )

    legend_handles = [
        mpatches.Patch(color=c, label=e) for e, c in edge_colors_map.items()
    ]
    ax.legend(
        handles=legend_handles, loc="lower left", fontsize=8, ncol=2, title="Edge Types"
    )
    ax.set_title(
        "MC1 Graph Schema: Node Types & Edge Types", fontsize=14, fontweight="bold"
    )
    ax.axis("off")
    plt.tight_layout()
    fig
    return


@app.cell
def _(json, pd):
    import pathlib

    _here = pathlib.Path(__file__).parent
    with open(_here / "MC1_graph.json", "r") as f:
        data = json.load(f)

    df_all_nodes = pd.DataFrame(data["nodes"])
    df_all_edges = pd.DataFrame(data["links"])

    # Lookup dicts
    id_to_name = dict(zip(df_all_nodes["id"], df_all_nodes["name"]))
    id_to_type = dict(zip(df_all_nodes["id"], df_all_nodes["Node Type"]))

    # Resolve names on edges once
    df_all_edges["source_name"] = df_all_edges["source"].map(id_to_name)
    df_all_edges["target_name"] = df_all_edges["target"].map(id_to_name)

    print(f"Nodes: {len(df_all_nodes)}  |  Edges: {len(df_all_edges)}")
    print(f"\nNode types:\n{df_all_nodes['Node Type'].value_counts().to_string()}")
    print(f"\nEdge types:\n{df_all_edges['Edge Type'].value_counts().to_string()}")
    return df_all_edges, df_all_nodes, id_to_name, id_to_type


@app.cell
def _(df_all_nodes):
    # Songs
    song_cols = [
        "id",
        "name",
        "genre",
        "release_date",
        "single",
        "notable",
        "notoriety_date",
        "written_date",
    ]
    song_cols = [c for c in song_cols if c in df_all_nodes.columns]
    df_songs = (
        df_all_nodes[df_all_nodes["Node Type"] == "Song"][song_cols]
        .copy()
        .reset_index(drop=True)
    )
    print(f"df_songs: {df_songs.shape}")
    # df_songs
    return (df_songs,)


@app.cell
def _(df_all_nodes):
    # Albums
    album_cols = [
        "id",
        "name",
        "genre",
        "release_date",
        "notable",
        "notoriety_date",
        "written_date",
    ]
    album_cols = [c for c in album_cols if c in df_all_nodes.columns]
    df_albums = (
        df_all_nodes[df_all_nodes["Node Type"] == "Album"][album_cols]
        .copy()
        .reset_index(drop=True)
    )
    print(f"df_albums: {df_albums.shape}")
    # df_albums
    return (df_albums,)


@app.cell
def _(df_all_nodes):
    # Persons
    person_cols = ["id", "name", "stage_name"]
    person_cols = [c for c in person_cols if c in df_all_nodes.columns]
    df_persons = (
        df_all_nodes[df_all_nodes["Node Type"] == "Person"][person_cols]
        .copy()
        .reset_index(drop=True)
    )
    print(f"df_persons: {df_persons.shape}")
    # df_persons
    return (df_persons,)


@app.cell
def _(df_all_nodes):
    # Musical Groups
    df_groups = (
        df_all_nodes[df_all_nodes["Node Type"] == "MusicalGroup"][["id", "name"]]
        .copy()
        .reset_index(drop=True)
    )
    print(f"df_groups: {df_groups.shape}")
    # df_groups
    return (df_groups,)


@app.cell
def _(df_all_nodes):
    # Record Labels
    df_labels = (
        df_all_nodes[df_all_nodes["Node Type"] == "RecordLabel"][["id", "name"]]
        .copy()
        .reset_index(drop=True)
    )
    print(f"df_labels: {df_labels.shape}")
    # df_labels
    return (df_labels,)


@app.cell
def _(df_all_edges, id_to_type):
    # Resolve source/target types on edges for filtering
    df_all_edges["source_type"] = df_all_edges["source"].map(id_to_type)
    df_all_edges["target_type"] = df_all_edges["target"].map(id_to_type)

    def agg_incoming(edge_type, node_ids, source_type=None):
        """Aggregate incoming edges (other -> node) as lists, optionally filtered by source type."""
        mask = (df_all_edges["Edge Type"] == edge_type) & (
            df_all_edges["target"].isin(node_ids)
        )
        if source_type:
            mask = mask & (df_all_edges["source_type"] == source_type)
        subset = df_all_edges[mask]
        return subset.groupby("target")["source_name"].apply(list)

    def agg_outgoing(edge_type, node_ids, target_type=None):
        """Aggregate outgoing edges (node -> other) as lists, optionally filtered by target type."""
        mask = (df_all_edges["Edge Type"] == edge_type) & (
            df_all_edges["source"].isin(node_ids)
        )
        if target_type:
            mask = mask & (df_all_edges["target_type"] == target_type)
        subset = df_all_edges[mask]
        return subset.groupby("source")["target_name"].apply(list)
    return agg_incoming, agg_outgoing


@app.cell
def _(agg_incoming, agg_outgoing, df_songs):
    song_ids = set(df_songs['id'])
    df_song_edges = df_songs.copy()

    # PerformerOf: source Person or MusicalGroup -> Song
    df_song_edges['performed_by_persons'] = df_song_edges['id'].map(agg_incoming('PerformerOf', song_ids, 'Person'))
    df_song_edges['performed_by_groups']  = df_song_edges['id'].map(agg_incoming('PerformerOf', song_ids, 'MusicalGroup'))

    # ComposerOf: source Person -> Song
    df_song_edges['composed_by'] = df_song_edges['id'].map(agg_incoming('ComposerOf', song_ids, 'Person'))

    # ProducerOf: source Person or RecordLabel -> Song
    df_song_edges['produced_by_persons'] = df_song_edges['id'].map(agg_incoming('ProducerOf', song_ids, 'Person'))
    df_song_edges['produced_by_labels']  = df_song_edges['id'].map(agg_incoming('ProducerOf', song_ids, 'RecordLabel'))

    # LyricistOf: source Person -> Song
    df_song_edges['lyrics_by'] = df_song_edges['id'].map(agg_incoming('LyricistOf', song_ids, 'Person'))

    # RecordedBy: Song -> RecordLabel
    df_song_edges['recorded_by'] = df_song_edges['id'].map(agg_outgoing('RecordedBy', song_ids, 'RecordLabel'))

    # DistributedBy: Song -> RecordLabel
    df_song_edges['distributed_by'] = df_song_edges['id'].map(agg_outgoing('DistributedBy', song_ids, 'RecordLabel'))

    # InStyleOf: Song -> Song, Album, Person, or MusicalGroup
    df_song_edges['in_style_of_songs']   = df_song_edges['id'].map(agg_outgoing('InStyleOf', song_ids, 'Song'))
    df_song_edges['in_style_of_albums']  = df_song_edges['id'].map(agg_outgoing('InStyleOf', song_ids, 'Album'))
    df_song_edges['in_style_of_persons'] = df_song_edges['id'].map(agg_outgoing('InStyleOf', song_ids, 'Person'))
    df_song_edges['in_style_of_groups']  = df_song_edges['id'].map(agg_outgoing('InStyleOf', song_ids, 'MusicalGroup'))

    # InterpolatesFrom: Song -> Song or Album
    df_song_edges['interpolates_from_songs']  = df_song_edges['id'].map(agg_outgoing('InterpolatesFrom', song_ids, 'Song'))
    df_song_edges['interpolates_from_albums'] = df_song_edges['id'].map(agg_outgoing('InterpolatesFrom', song_ids, 'Album'))

    # CoverOf: Song -> Song or Album
    df_song_edges['cover_of_songs']  = df_song_edges['id'].map(agg_outgoing('CoverOf', song_ids, 'Song'))
    df_song_edges['cover_of_albums'] = df_song_edges['id'].map(agg_outgoing('CoverOf', song_ids, 'Album'))

    # LyricalReferenceTo: Song -> Song or Album
    df_song_edges['lyrical_ref_to_songs']  = df_song_edges['id'].map(agg_outgoing('LyricalReferenceTo', song_ids, 'Song'))
    df_song_edges['lyrical_ref_to_albums'] = df_song_edges['id'].map(agg_outgoing('LyricalReferenceTo', song_ids, 'Album'))

    # DirectlySamples: Song -> Song or Album
    df_song_edges['directly_samples_songs']  = df_song_edges['id'].map(agg_outgoing('DirectlySamples', song_ids, 'Song'))
    df_song_edges['directly_samples_albums'] = df_song_edges['id'].map(agg_outgoing('DirectlySamples', song_ids, 'Album'))

    print(f"df_song_edges: {df_song_edges.shape}")
    # df_song_edges
    return (df_song_edges,)


@app.cell
def _(agg_incoming, agg_outgoing, df_albums):
    # Album edge table — every source/target type gets its own column per the PDF schema
    album_ids = set(df_albums['id'])
    df_album_edges = df_albums.copy()

    # PerformerOf: source Person or MusicalGroup -> Album
    df_album_edges['performed_by_persons'] = df_album_edges['id'].map(agg_incoming('PerformerOf', album_ids, 'Person'))
    df_album_edges['performed_by_groups']  = df_album_edges['id'].map(agg_incoming('PerformerOf', album_ids, 'MusicalGroup'))

    # ComposerOf: source Person -> Album
    df_album_edges['composed_by'] = df_album_edges['id'].map(agg_incoming('ComposerOf', album_ids, 'Person'))

    # ProducerOf: source Person or RecordLabel -> Album
    df_album_edges['produced_by_persons'] = df_album_edges['id'].map(agg_incoming('ProducerOf', album_ids, 'Person'))
    df_album_edges['produced_by_labels']  = df_album_edges['id'].map(agg_incoming('ProducerOf', album_ids, 'RecordLabel'))

    # LyricistOf: source Person -> Album
    df_album_edges['lyrics_by'] = df_album_edges['id'].map(agg_incoming('LyricistOf', album_ids, 'Person'))

    # RecordedBy: Album -> RecordLabel
    df_album_edges['recorded_by'] = df_album_edges['id'].map(agg_outgoing('RecordedBy', album_ids, 'RecordLabel'))

    # DistributedBy: Album -> RecordLabel
    df_album_edges['distributed_by'] = df_album_edges['id'].map(agg_outgoing('DistributedBy', album_ids, 'RecordLabel'))

    # InStyleOf: Album -> Song, Album, Person, or MusicalGroup
    df_album_edges['in_style_of_songs']   = df_album_edges['id'].map(agg_outgoing('InStyleOf', album_ids, 'Song'))
    df_album_edges['in_style_of_albums']  = df_album_edges['id'].map(agg_outgoing('InStyleOf', album_ids, 'Album'))
    df_album_edges['in_style_of_persons'] = df_album_edges['id'].map(agg_outgoing('InStyleOf', album_ids, 'Person'))
    df_album_edges['in_style_of_groups']  = df_album_edges['id'].map(agg_outgoing('InStyleOf', album_ids, 'MusicalGroup'))

    # InterpolatesFrom: Album -> Song or Album
    df_album_edges['interpolates_from_songs']  = df_album_edges['id'].map(agg_outgoing('InterpolatesFrom', album_ids, 'Song'))
    df_album_edges['interpolates_from_albums'] = df_album_edges['id'].map(agg_outgoing('InterpolatesFrom', album_ids, 'Album'))

    # CoverOf: Album -> Song or Album
    df_album_edges['cover_of_songs']  = df_album_edges['id'].map(agg_outgoing('CoverOf', album_ids, 'Song'))
    df_album_edges['cover_of_albums'] = df_album_edges['id'].map(agg_outgoing('CoverOf', album_ids, 'Album'))

    # LyricalReferenceTo: Album -> Song or Album
    df_album_edges['lyrical_ref_to_songs']  = df_album_edges['id'].map(agg_outgoing('LyricalReferenceTo', album_ids, 'Song'))
    df_album_edges['lyrical_ref_to_albums'] = df_album_edges['id'].map(agg_outgoing('LyricalReferenceTo', album_ids, 'Album'))

    # DirectlySamples: Album -> Song or Album
    df_album_edges['directly_samples_songs']  = df_album_edges['id'].map(agg_outgoing('DirectlySamples', album_ids, 'Song'))
    df_album_edges['directly_samples_albums'] = df_album_edges['id'].map(agg_outgoing('DirectlySamples', album_ids, 'Album'))

    print(f"df_album_edges: {df_album_edges.shape}")
    # df_album_edges
    return (df_album_edges,)


@app.cell
def _(agg_incoming, agg_outgoing, df_persons):
    # Person edge table — split by every possible target type per the PDF schema
    person_ids = set(df_persons["id"])
    df_person_edges = df_persons.copy()

    # PerformerOf: Person -> Song or Album
    df_person_edges["performer_of_songs"] = df_person_edges["id"].map(
        agg_outgoing("PerformerOf", person_ids, "Song")
    )
    df_person_edges["performer_of_albums"] = df_person_edges["id"].map(
        agg_outgoing("PerformerOf", person_ids, "Album")
    )

    # ComposerOf: Person -> Song or Album
    df_person_edges["composer_of_songs"] = df_person_edges["id"].map(
        agg_outgoing("ComposerOf", person_ids, "Song")
    )
    df_person_edges["composer_of_albums"] = df_person_edges["id"].map(
        agg_outgoing("ComposerOf", person_ids, "Album")
    )

    # ProducerOf: Person -> Song, Album, Person, or MusicalGroup
    df_person_edges["producer_of_songs"] = df_person_edges["id"].map(
        agg_outgoing("ProducerOf", person_ids, "Song")
    )
    df_person_edges["producer_of_albums"] = df_person_edges["id"].map(
        agg_outgoing("ProducerOf", person_ids, "Album")
    )
    df_person_edges["producer_of_persons"] = df_person_edges["id"].map(
        agg_outgoing("ProducerOf", person_ids, "Person")
    )
    df_person_edges["producer_of_groups"] = df_person_edges["id"].map(
        agg_outgoing("ProducerOf", person_ids, "MusicalGroup")
    )

    # LyricistOf: Person -> Song or Album
    df_person_edges["lyricist_of_songs"] = df_person_edges["id"].map(
        agg_outgoing("LyricistOf", person_ids, "Song")
    )
    df_person_edges["lyricist_of_albums"] = df_person_edges["id"].map(
        agg_outgoing("LyricistOf", person_ids, "Album")
    )

    # MemberOf: Person -> MusicalGroup
    df_person_edges["member_of"] = df_person_edges["id"].map(
        agg_outgoing("MemberOf", person_ids, "MusicalGroup")
    )

    # Incoming: Person can be produced by another Person or RecordLabel
    df_person_edges["produced_by_persons"] = df_person_edges["id"].map(
        agg_incoming("ProducerOf", person_ids, "Person")
    )
    df_person_edges["produced_by_labels"] = df_person_edges["id"].map(
        agg_incoming("ProducerOf", person_ids, "RecordLabel")
    )

    print(f"df_person_edges: {df_person_edges.shape}")
    # df_person_edges
    return (df_person_edges,)


@app.cell
def _(agg_incoming, agg_outgoing, df_groups):
    # Musical Group edge table — split by every possible source/target type per the PDF schema
    group_ids = set(df_groups["id"])
    df_group_edges = df_groups.copy()

    # PerformerOf: MusicalGroup -> Song or Album
    df_group_edges["performer_of_songs"] = df_group_edges["id"].map(
        agg_outgoing("PerformerOf", group_ids, "Song")
    )
    df_group_edges["performer_of_albums"] = df_group_edges["id"].map(
        agg_outgoing("PerformerOf", group_ids, "Album")
    )

    # Incoming MemberOf: Person -> MusicalGroup
    df_group_edges["members"] = df_group_edges["id"].map(
        agg_incoming("MemberOf", group_ids, "Person")
    )

    # Incoming ProducerOf: Person or RecordLabel -> MusicalGroup
    df_group_edges["produced_by_persons"] = df_group_edges["id"].map(
        agg_incoming("ProducerOf", group_ids, "Person")
    )
    df_group_edges["produced_by_labels"] = df_group_edges["id"].map(
        agg_incoming("ProducerOf", group_ids, "RecordLabel")
    )

    print(f"df_group_edges: {df_group_edges.shape}")
    # df_group_edges
    return (df_group_edges,)


@app.cell
def _(agg_incoming, agg_outgoing, df_labels):
    # Record Label edge table — split by every possible source/target type per the PDF schema
    label_ids = set(df_labels["id"])
    df_label_edges = df_labels.copy()

    # Incoming RecordedBy: Song or Album -> RecordLabel (split by source type)
    df_label_edges["recorded_songs"] = df_label_edges["id"].map(
        agg_incoming("RecordedBy", label_ids, "Song")
    )
    df_label_edges["recorded_albums"] = df_label_edges["id"].map(
        agg_incoming("RecordedBy", label_ids, "Album")
    )

    # Incoming DistributedBy: Song or Album -> RecordLabel (split by source type)
    df_label_edges["distributed_songs"] = df_label_edges["id"].map(
        agg_incoming("DistributedBy", label_ids, "Song")
    )
    df_label_edges["distributed_albums"] = df_label_edges["id"].map(
        agg_incoming("DistributedBy", label_ids, "Album")
    )

    # ProducerOf: RecordLabel -> Song, Album, Person, or MusicalGroup
    df_label_edges["producer_of_songs"] = df_label_edges["id"].map(
        agg_outgoing("ProducerOf", label_ids, "Song")
    )
    df_label_edges["producer_of_albums"] = df_label_edges["id"].map(
        agg_outgoing("ProducerOf", label_ids, "Album")
    )
    df_label_edges["producer_of_persons"] = df_label_edges["id"].map(
        agg_outgoing("ProducerOf", label_ids, "Person")
    )
    df_label_edges["producer_of_groups"] = df_label_edges["id"].map(
        agg_outgoing("ProducerOf", label_ids, "MusicalGroup")
    )

    print(f"df_label_edges: {df_label_edges.shape}")
    # df_label_edges
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## Summary
    | Table | Contents |
    |---|---|
    | `df_song_edges` | performed_by_persons, performed_by_groups, composed_by, produced_by_persons, produced_by_labels, lyrics_by, recorded_by, distributed_by |
    | `df_album_edges` | same authorship/label columns as songs |
    | `df_person_edges` | performer_of_songs/albums, composer_of_songs/albums, producer_of_songs/albums/persons/groups, lyricist_of_songs/albums, member_of, produced_by_persons/labels |
    | `df_group_edges` | performer_of_songs/albums, members, produced_by_persons/labels |
    | `df_label_edges` | recorded_songs/albums, distributed_songs/albums, producer_of_songs/albums/persons/groups |
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    # Q1
    *Design and develop visualizations and visual analytic tools that will allow Silas to explore and understand the profile of Sailor Shift’s career*

    a. Who has she been most influenced by over time?
    **Streamgraph + Bar Chart**

    b. Who has she collaborated with and directly or indirectly influenced?
    **Network Graph**

    c. How has she influenced collaborators of the broader Oceanus Folk community?
    **Area Chart**


    **Main Variables of Interest**
    - to_sailor: Sailor's own works reference another artist
    - from_sailor: other artist's works reference Sailor
    - hop1: directly influenced artists to/from Sailor
    - hop2: identifies the artists that the hop1 artists influenced
    """)
    return


@app.cell
def _():
    AUTHORSHIP_TYPES = {'ComposerOf', 'PerformerOf', 'LyricistOf', 'ProducerOf'}
    INFLUENCE_TYPES = {'InStyleOf', 'InterpolatesFrom', 'CoverOf', 'DirectlySamples', 'LyricalReferenceTo'}
    PERSON_TYPES = {'Person', 'MusicalGroup'}
    WORK_TYPES = {'Song', 'Album'}
    return AUTHORSHIP_TYPES, INFLUENCE_TYPES, PERSON_TYPES, WORK_TYPES


@app.cell
def _(df_person_edges):
    # Finding Sailor Shift node
    def find_sailor(df_person_edges):
        row = df_person_edges[df_person_edges['name'].str.contains('Sailor Shift', case=False, na=False)].iloc[0]
        return row['id'], row['name']

    q1_sailor_id, q1_sailor_name = find_sailor(df_person_edges)
    print(f"Found Sailor Shift: {q1_sailor_name} (ID: {q1_sailor_id})")
    return q1_sailor_id, q1_sailor_name


@app.cell
def _(AUTHORSHIP_TYPES, df_all_edges, df_all_nodes, df_songs, q1_sailor_id):
    def get_sailor_songs(df_all_edges, df_all_nodes, df_songs, q1_sailor_id):

        song_id_set = set(df_songs['id'])

        # Songs Sailor is directly credited on
        sailor_direct = df_all_edges[
            (df_all_edges['source'] == q1_sailor_id) &
            (df_all_edges['Edge Type'].isin(AUTHORSHIP_TYPES)) &
            (df_all_edges['target'].isin(song_id_set))
        ][['target', 'Edge Type']].rename(columns={'target': 'id', 'Edge Type': 'role'})

        solo_song_ids = set(sailor_direct['id'])

        # Find Ivy Echos group node ID
        ivy_row = df_all_nodes[
            (df_all_nodes['name'].str.lower().str.contains('ivy echo', na=False)) &
            (df_all_nodes['Node Type'] == 'MusicalGroup')
        ]
        ivy_echos_ids = set(ivy_row['id']) if not ivy_row.empty else set()

        # Songs Ivy Echos performed
        ivy_song_ids = set()
        if ivy_echos_ids:
            ivy_songs = df_all_edges[
                (df_all_edges['source'].isin(ivy_echos_ids)) &
                (df_all_edges['Edge Type'].isin(AUTHORSHIP_TYPES)) &
                (df_all_edges['target'].isin(song_id_set))
            ]['target']
            ivy_song_ids = set(ivy_songs)

        all_song_ids = solo_song_ids | ivy_song_ids

        # Build the output table from df_songs metadata
        df_sailor_songs = df_songs[df_songs['id'].isin(all_song_ids)].copy()

        return all_song_ids, df_sailor_songs.sort_values('release_date').reset_index(drop=True)

    all_song_ids, df_sailor_songs = get_sailor_songs(df_all_edges, df_all_nodes, df_songs, q1_sailor_id)

    # print(f"Total songs: {len(df_sailor_songs)}")
    # df_sailor_songs
    return (all_song_ids,)


@app.cell
def _(AUTHORSHIP_TYPES, df_albums, df_all_edges, df_all_nodes, q1_sailor_id):
    def get_sailor_albums(df_all_edges, df_all_nodes, df_albums, q1_sailor_id):

        album_id_set = set(df_albums['id'])

        # Albums Sailor is directly credited on
        sailor_direct = df_all_edges[
            (df_all_edges['source'] == q1_sailor_id) &
            (df_all_edges['Edge Type'].isin(AUTHORSHIP_TYPES)) &
            (df_all_edges['target'].isin(album_id_set))
        ][['target', 'Edge Type']].rename(columns={'target': 'id', 'Edge Type': 'role'})

        solo_album_ids = set(sailor_direct['id'])

        # Albums credited to Ivy Echoes
        ivy_row = df_all_nodes[
            (df_all_nodes['name'].str.lower().str.contains('ivy echo', na=False)) &
            (df_all_nodes['Node Type'] == 'MusicalGroup')
        ]
        ivy_echos_ids = set(ivy_row['id']) if not ivy_row.empty else set()

        ivy_album_ids = set()
        if ivy_echos_ids:
            ivy_album_ids = set(
                df_all_edges[
                    (df_all_edges['source'].isin(ivy_echos_ids)) &
                    (df_all_edges['Edge Type'].isin(AUTHORSHIP_TYPES)) &
                    (df_all_edges['target'].isin(album_id_set))
                ]['target']
            )

        all_album_ids = solo_album_ids | ivy_album_ids

        # Build the output table from df_albums metadata
        df_sailor_albums = df_albums[df_albums['id'].isin(all_album_ids)].copy()

        return all_album_ids, ivy_echos_ids, df_sailor_albums.sort_values('release_date').reset_index(drop=True)

    all_album_ids, ivy_echos_ids, df_sailor_albums = get_sailor_albums(df_all_edges, df_all_nodes, df_albums, q1_sailor_id)

    # print(f"Total albums: {len(df_sailor_albums)}")
    # df_sailor_albums
    return all_album_ids, ivy_echos_ids


@app.cell
def _(
    INFLUENCE_TYPES,
    all_album_ids,
    all_song_ids,
    df_all_edges,
    df_all_nodes,
    ivy_echos_ids,
    pd,
    q1_sailor_id,
):
    def build_influence_edges(sailor_work_ids, sailor_entity_ids, df_all_edges, df_all_nodes):

        # Year lookup from release_date across all nodes
        year_lookup = (
            df_all_nodes.set_index('id')['release_date'].str[:4]
            .apply(pd.to_numeric, errors='coerce').dropna().astype(int).to_dict()
        )

        # Sailor's works are the source — edges point to what influenced her
        to_sailor = df_all_edges[
            (df_all_edges['source'].isin(sailor_work_ids)) &
            (df_all_edges['Edge Type'].isin(INFLUENCE_TYPES))
        ].copy()
        to_sailor['direction'] = 'to_sailor'

        # Sailor is the target — external sources influenced by her
        from_sailor = df_all_edges[
            (
                df_all_edges['target'].isin(sailor_work_ids) |
                df_all_edges['target'].isin(sailor_entity_ids)
            ) &
            (df_all_edges['Edge Type'].isin(INFLUENCE_TYPES)) &
            (~df_all_edges['source'].isin(sailor_entity_ids))
        ].copy()
        from_sailor['direction'] = 'from_sailor'

        # Building the influence connections
        q1_df_influence_edges = (
            pd.concat([to_sailor, from_sailor], ignore_index=True)
            .rename(columns={'Edge Type': 'edge_type'})
            [['source', 'source_name', 'source_type',
              'target', 'target_type',
              'edge_type', 'direction']]
        )

        q1_df_influence_edges['year'] = q1_df_influence_edges['source'].map(year_lookup)

        return q1_df_influence_edges

    # Collect all Sailor's IDs
    sailor_work_ids   = all_song_ids | all_album_ids
    sailor_entity_ids = {q1_sailor_id} | ivy_echos_ids

    q1_df_influence_edges = build_influence_edges(sailor_work_ids, sailor_entity_ids, df_all_edges, df_all_nodes)
    # print(f"Total influence edges: {len(q1_df_influence_edges)}")
    # print(q1_df_influence_edges['direction'].value_counts().to_string())
    # q1_df_influence_edges
    return q1_df_influence_edges, sailor_entity_ids, sailor_work_ids


@app.cell
def _(
    AUTHORSHIP_TYPES,
    PERSON_TYPES,
    WORK_TYPES,
    df_all_edges,
    df_all_nodes,
    pd,
    q1_df_influence_edges,
    sailor_entity_ids,
):
    def build_artist_influence(df_all_edges, df_all_nodes, q1_df_influence_edges, sailor_entity_ids):

        # genre lookup
        work_genre = df_all_nodes.set_index('id')['genre'].dropna().to_dict()

        # Work -> artist lookup
        auth = (
            df_all_edges[
                (df_all_edges['Edge Type'].isin(AUTHORSHIP_TYPES)) &
                (df_all_edges['source_type'].isin(PERSON_TYPES))
            ]
            [['source', 'source_name', 'source_type', 'target']]
            .rename(columns={
                'source': 'artist_id',
                'source_name': 'artist_name',
                'source_type': 'artist_type',
                'target': 'work_id',
            })
            .drop_duplicates(subset=['artist_id', 'work_id'])
        )

        # to_sailor: Sailor's work is the source; target is the work that influenced her
        to_s = q1_df_influence_edges[q1_df_influence_edges['direction'] == 'to_sailor']
        resolved_to = (
            to_s[to_s['target_type'].isin(WORK_TYPES)]
            .merge(auth.rename(columns={'work_id': 'target'}), on='target', how='left')
            [['artist_id', 'artist_name', 'artist_type', 'target', 'edge_type', 'direction', 'year']]
            .rename(columns={'target': 'work_id'})
        )

        # from_sailor: Sailor is the target; source is who/what references her
        from_s = q1_df_influence_edges[q1_df_influence_edges['direction'] == 'from_sailor']
        direct_from = (
            from_s[from_s['source_type'].isin(PERSON_TYPES)]
            [['source', 'source_name', 'source_type', 'edge_type', 'direction', 'year']]
            .rename(columns={'source': 'artist_id', 'source_name': 'artist_name', 'source_type': 'artist_type'})
            .assign(work_id=None)
        )
        resolved_from = (
            from_s[from_s['source_type'].isin(WORK_TYPES)]
            .merge(auth.rename(columns={'work_id': 'source'}), on='source', how='left')
            [['artist_id', 'artist_name', 'artist_type', 'source', 'edge_type', 'direction', 'year']]
            .rename(columns={'source': 'work_id'})
        )

        combined = pd.concat([resolved_to, direct_from, resolved_from], ignore_index=True)
        df_influence_artists = (
            combined[~combined['artist_id'].isin(sailor_entity_ids)]
            [['artist_id', 'artist_name', 'artist_type', 'work_id', 'edge_type', 'direction', 'year']]
            .reset_index(drop=True)
        )

        # genre of the influence-carrying work
        df_influence_artists['genre'] = df_influence_artists['work_id'].map(work_genre)
        df_influence_artists = df_influence_artists.drop(columns=['work_id'])

        return df_influence_artists, auth, work_genre

    df_influence_artists, auth_full, work_genre = build_artist_influence(df_all_edges, df_all_nodes, q1_df_influence_edges, sailor_entity_ids)
    # print(f"df_influence_artists: {df_influence_artists.shape}")
    # print("direction:",  df_influence_artists['direction'].value_counts().to_string())
    # df_influence_artists
    return auth_full, df_influence_artists, work_genre


@app.cell
def _(
    Counter,
    INFLUENCE_TYPES,
    WORK_TYPES,
    auth_full,
    df_all_edges,
    df_influence_artists,
    pd,
    sailor_entity_ids,
    work_genre,
):
    def build_network(df_all_edges, df_influence_artists, sailor_entity_ids, auth_full, work_genre):

        # Work -> artist mapping for hop-2 (auth_full shared from build_artist_influence)
        auth_df = auth_full[['artist_id', 'work_id']]
        artist_to_works = auth_df.groupby('artist_id')['work_id'].apply(set).to_dict()

        # All influence edges for hop-2
        all_inf = df_all_edges[df_all_edges['Edge Type'].isin(INFLUENCE_TYPES)]

        # hop-1: artists who reference Sailor (from_sailor direction in df_influence_artists)
        hop1_from = (
            set(df_influence_artists[df_influence_artists['direction'] == 'from_sailor']['artist_id'].dropna())
            - sailor_entity_ids
        )

        # Collect all works by hop-1 artists, then find what those works influenced
        hop1_from_works = set().union(*[artist_to_works.get(a, set()) for a in hop1_from]) if hop1_from else set()
        h2_from_raw = all_inf[all_inf['source'].isin(hop1_from_works)].copy()

        # hop-2: artists behind the works influenced by hop-1 works
        hop2_from = (
            set(
                h2_from_raw[h2_from_raw['target_type'].isin(WORK_TYPES)]
                .merge(auth_df.rename(columns={'work_id': 'target', 'artist_id': 'hop2_artist'}),
                       on='target', how='left')
                ['hop2_artist'].dropna().unique()
            )
            - sailor_entity_ids - hop1_from
        )

        # primary_genre: modal genre across all of an artist's works
        def primary_genre(artist_id):
            works = artist_to_works.get(artist_id, set())
            genres = [work_genre[w] for w in works if w in work_genre]
            return Counter(genres).most_common(1)[0][0] if genres else None

        # Edge table: one row per artist per hop
        hop2_rows = pd.DataFrame([
            {'artist_id': aid, 'direction': 'from_sailor', 'hop': 2}
            for aid in hop2_from
        ])
        df_network_edges = pd.concat(
            [df_influence_artists[['artist_id', 'direction']].assign(hop=1), hop2_rows],
            ignore_index=True,
        )
        df_network_edges = df_network_edges[~df_network_edges['artist_id'].isin(sailor_entity_ids)].copy()

        # Node table: one row per unique artist with their primary genre
        df_network_nodes = (
            df_network_edges[['artist_id']]
            .drop_duplicates()
            .assign(primary_genre=lambda d: d['artist_id'].map(primary_genre))
            .reset_index(drop=True)
        )

        # Bridge table: hop1 -> hop2 artist pairs
        work_to_hop1_from = {w: a for a in hop1_from for w in artist_to_works.get(a, set())}
        df_bridges = (
            h2_from_raw[h2_from_raw['target_type'].isin(WORK_TYPES)]
            [['source', 'target']]
            .merge(auth_df.rename(columns={'work_id': 'target', 'artist_id': 'hop2_artist_id'}),
                   on='target', how='left')
            .assign(hop1_artist_id=lambda d: d['source'].map(work_to_hop1_from))
            [['hop1_artist_id', 'hop2_artist_id']]
            .dropna()
            .drop_duplicates()
            .loc[lambda d: ~d['hop2_artist_id'].isin(sailor_entity_ids | hop1_from)]
            .reset_index(drop=True)
            .assign(direction='from_sailor',
                    hop2_genre=lambda d: d['hop2_artist_id'].map(primary_genre))
        )

        # Genre lookup for every artist with any authorship edge
        artist_genre = {a: primary_genre(a) for a in artist_to_works}

        return df_network_edges, df_network_nodes, df_bridges, artist_genre

    df_network_edges, df_network_nodes, df_bridges, artist_genre = build_network(df_all_edges, df_influence_artists, sailor_entity_ids, auth_full, work_genre)

    # print(f"df_network_edges: {df_network_edges.shape}")
    # print("hop:", df_network_edges['hop'].value_counts().to_string())
    # print(f"df_network_nodes: {df_network_nodes.shape}")
    # df_network_edges
    return artist_genre, df_bridges, df_network_edges


@app.cell
def _(
    AUTHORSHIP_TYPES,
    PERSON_TYPES,
    df_all_edges,
    q1_sailor_id,
    sailor_entity_ids,
    sailor_work_ids,
):
    def sailor_collaborations(df_all_edges, q1_sailor_id, sailor_entity_ids, sailor_work_ids):

        # All authorship credits on Sailor's works, excluding Sailor and Ivy Echos themselves
        df_collaborators = (
            df_all_edges[
                (df_all_edges['target'].isin(sailor_work_ids)) &
                (df_all_edges['Edge Type'].isin(AUTHORSHIP_TYPES)) &
                (df_all_edges['source_type'].isin(PERSON_TYPES)) &
                (~df_all_edges['source'].isin(sailor_entity_ids))
            ]
            [['source', 'source_name', 'source_type', 'target']]
            .rename(columns={
                'source': 'collaborator_id',
                'source_name': 'collaborator_name',
                'source_type': 'collaborator_type',
                'target': 'work_id',
            })
            .drop_duplicates(subset=['collaborator_id', 'work_id'])
            .reset_index(drop=True)
        )

        return df_collaborators

    df_collaborators = sailor_collaborations(df_all_edges, q1_sailor_id, sailor_entity_ids, sailor_work_ids)

    # print(f"Total co-credits: {len(df_collaborators)}")
    # print(f"Unique collaborators: {df_collaborators['collaborator_id'].nunique()}")
    # print("Top collaborators:", df_collaborators['collaborator_name'].value_counts().head(10).to_string())
    # df_collaborators
    return (df_collaborators,)


@app.cell
def _(
    AUTHORSHIP_TYPES,
    PERSON_TYPES,
    WORK_TYPES,
    df_all_edges,
    df_all_nodes,
    df_network_edges,
    pd,
    sailor_entity_ids,
):
    def build_oceanus_community(df_all_nodes, df_all_edges, df_network_edges, sailor_entity_ids):

        # All Oceanus Folk works (Song or Album)
        of_work_ids = set(
            df_all_nodes[
                (df_all_nodes['genre'] == 'Oceanus Folk') &
                (df_all_nodes['Node Type'].isin(WORK_TYPES))
            ]['id']
        )

        # All artists credited on any Oceanus Folk work (excluding Sailor/Ivy Echos)
        of_credits = (
            df_all_edges[
                (df_all_edges['target'].isin(of_work_ids)) &
                (df_all_edges['Edge Type'].isin(AUTHORSHIP_TYPES)) &
                (df_all_edges['source_type'].isin(PERSON_TYPES)) &
                (~df_all_edges['source'].isin(sailor_entity_ids))
            ]
            [['source', 'source_name', 'source_type', 'target']]
            .rename(columns={
                'source': 'artist_id',
                'source_name': 'artist_name',
                'source_type': 'artist_type',
                'target': 'work_id',
            })
        )

        # Work metadata for release dates
        meta_cols = ['id', 'release_date']
        work_meta = (
            df_all_nodes[df_all_nodes['id'].isin(of_work_ids)]
            [meta_cols]
            .rename(columns={'id': 'work_id'})
        )
        of_credits = of_credits.merge(work_meta, on='work_id', how='left')
        of_credits['release_year'] = pd.to_numeric(
            of_credits['release_date'].astype(str).str[:4], errors='coerce'
        )

        # Deduplicated credits (one row per artist-work, with a known release year)
        of_credits_dedup = (
            of_credits.dropna(subset=['release_year'])
            .drop_duplicates(subset=['artist_id', 'work_id'])
        )

        # Per-artist yearly OF work counts -> cumulative trajectory
        yearly = (
            of_credits_dedup
            .groupby(['artist_id', 'artist_name', 'artist_type', 'release_year'])
            .agg(yearly_count=('work_id', 'nunique'))
            .reset_index()
            .sort_values(['artist_id', 'release_year'])
        )
        # Per-artist totals (for Q3 tooltip)
        agg = {'of_work_count': ('work_id', 'nunique')}
        artist_totals = (
            of_credits_dedup
            .groupby('artist_id')
            .agg(**agg)
            .reset_index()
        )

        # Influence flag — which OF artists did Sailor influence
        influenced_by_sailor_ids = set(
            df_network_edges[df_network_edges['direction'] == 'from_sailor']['artist_id'].dropna()
        )

        # Join per-year rows with totals and influence flag
        df_of_yearly = yearly.merge(artist_totals, on='artist_id', how='left')
        df_of_yearly['influenced_by_sailor'] = df_of_yearly['artist_id'].isin(influenced_by_sailor_ids)

        return df_of_yearly.sort_values(['artist_name', 'release_year']).reset_index(drop=True)

    df_of_yearly = build_oceanus_community(df_all_nodes, df_all_edges, df_network_edges, sailor_entity_ids)

    _n_artists = df_of_yearly['artist_id'].nunique()
    _n_influenced = df_of_yearly.drop_duplicates('artist_id')['influenced_by_sailor'].sum()
    # print(f"Oceanus Folk community: {_n_artists} artists ({len(df_of_yearly)} artist-year rows)")
    # print(f" influenced by Sailor: {_n_influenced}")
    # df_of_yearly
    return (df_of_yearly,)


@app.cell
def _():
    # Dashboard theme — shared across all visualizations
    background = "#ffffff"
    title = "#1a2d3e"
    tick = "#7bafd4"
    stream_colors = [
        "#89c4d4", "#7fc8a9", "#aed4e6", "#b2dfc5",
        "#5ba3c9", "#6dbf9e", "#c8dff0", "#a8d8c0",
        "#4a90bf", "#5aac8e", "#3478a5", "#3d8f72",
    ]
    node_color = {
        'Sailor': '#f9a825',
        'Collaborator': '#5ba3c9',
        'Directly influenced': '#6dbf9e',
        'Indirectly influenced': '#aed4e6',
    }
    return background, node_color, stream_colors, tick, title


@app.cell
def _(df_influence_artists, pd, stream_colors):
    # Q1 — pre-compute streamgraph data
    q1_base = (
        df_influence_artists[
            (df_influence_artists['direction'] == 'to_sailor') &
            df_influence_artists['year'].notna()
        ]
        .assign(year=lambda d: d['year'].astype(int))
        .copy()
    )
    q1_base['genre'] = q1_base['genre'].fillna('Unknown')

    _sg_raw = (
        q1_base[q1_base['genre'] != 'Unknown']
        .groupby(['year', 'genre'])
        .size()
        .reset_index(name='count')
    )

    _yrs = _sg_raw['year'].unique()
    _gns = _sg_raw['genre'].unique()
    sg_data = (
        _sg_raw.set_index(['year', 'genre'])
        .reindex(pd.MultiIndex.from_product([_yrs, _gns], names=['year', 'genre']), fill_value=0)
        .reset_index()
    )
    sorted_genres = sorted(sg_data['genre'].unique())
    genre_color_map = {g: stream_colors[i % len(stream_colors)] for i, g in enumerate(sorted_genres)}
    return genre_color_map, q1_base, sg_data, sorted_genres


@app.cell
def _(
    alt,
    background,
    genre_color_map,
    mo,
    sg_data,
    sorted_genres,
    tick,
    title,
):
    # Q1A — Streamgraph: who influenced Sailor over time?
    _sg_param = alt.selection_interval(name='q1_brush', encodings=['x'], empty=True)
    _x_sg_scale = alt.Scale(nice=False)

    q1_sg = (
        alt.Chart(sg_data)
        .mark_area(interpolate='monotone', opacity=0.8)
        .encode(
            x=alt.X('year:Q', scale=_x_sg_scale,
                    axis=alt.Axis(title='Year', grid=False, format='d',
                                  labelColor=title, titleColor=title, tickColor=tick,
                                  labelFontSize=12, titleFontSize=13)),
            y=alt.Y('count:Q', stack='center', axis=None),
            color=alt.Color('genre:N',
                            scale=alt.Scale(domain=sorted_genres,
                                            range=[genre_color_map[g] for g in sorted_genres]),
                            legend=alt.Legend(title='Genre', labelColor=title,
                                              titleColor=title, orient='right')),
            tooltip=[
                alt.Tooltip('genre:N', title='Genre'),
                alt.Tooltip('year:Q', title='Year')
            ]
        )
        .add_params(_sg_param)
        .properties(
            width=640, height=280,
            title=alt.TitleParams('Q1A — Who Has Sailor Shift Been Most Influenced By Over Time?',
                                  color=title, fontSize=14, fontWeight='bold')
            )
        )

    q1_sg_view = mo.ui.altair_chart(
        q1_sg.configure_view(fill=background, stroke=None, strokeWidth=0).configure(background=background)
    )
    return (q1_sg_view,)


@app.cell
def _(
    alt,
    background,
    genre_color_map,
    q1_base,
    q1_sg_view,
    sorted_genres,
    title,
):
    # Q1 bar chart - filtered by streamgraph brush
    _sel = q1_sg_view.value
    if len(_sel) > 0:
        _y0 = int(_sel['year'].min())
        _y1 = int(_sel['year'].max())
    else:
        _y0 = int(q1_base['year'].min())
        _y1 = int(q1_base['year'].max())

    _period = q1_base[
        (q1_base['year'] >= _y0) &
        (q1_base['year'] <= _y1) &
        q1_base['artist_name'].notna()
    ].copy()

    # Weighted influence score: based on how direct the influence is
    _weights = {
        'DirectlySamples': 5,
        'CoverOf': 4,
        'InterpolatesFrom': 3,
        'LyricalReferenceTo': 2,
        'InStyleOf': 1,
    }
    _period['influence_score'] = _period['edge_type'].map(_weights).fillna(1)

    top10 = (
        _period
        .groupby(['artist_id', 'artist_name', 'artist_type', 'genre'])['influence_score']
        .sum()
        .reset_index()
        .sort_values('influence_score', ascending=False)
        .head(10)
    )

    _max_score = int(top10['influence_score'].max()) if not top10.empty else 1

    _bar_domain = sorted_genres
    _bar_range  = [genre_color_map[g] for g in sorted_genres]

    q1_bar = (
        alt.Chart(top10)
        .mark_bar()
        .encode(
            y=alt.Y('artist_name:N', sort='-x',
                    axis=alt.Axis(title=None, labelColor=title, labelLimit=180)),
            x=alt.X('influence_score:Q',
                    scale=alt.Scale(domain=[0, _max_score], zero=True),
                    axis=alt.Axis(title='Influence score', labelColor=title,
                                  titleColor=title, grid=False)),
            color=alt.Color('genre:N',
                            scale=alt.Scale(domain=_bar_domain, range=_bar_range),
                            legend=alt.Legend(title='Top Genre', labelColor=title,
                                              titleColor=title)),
            tooltip=[
                alt.Tooltip('artist_name:N', title='Artist'),
                alt.Tooltip('artist_type:N', title='Type'),
                alt.Tooltip('genre:N', title='Genre'),
                alt.Tooltip('influence_score:Q', title='Influence score'),
            ]
        )
        .properties(
            width=240, height=280,
            title=alt.TitleParams(
                f'Top 10 Influencers ({_y0}–{_y1})',
                color=title, fontSize=14, fontWeight='bold'
            )
        )
        .configure_view(fill=background, stroke=None, strokeWidth=0)
        .configure(background=background)
    )
    return (q1_bar,)


@app.cell
def _(
    artist_genre,
    df_bridges,
    df_collaborators,
    df_influence_artists,
    id_to_name,
):
    # Q1B — Pre-compute all data
    _id_to_genre = artist_genre

    # All collaborators sorted by shared-work count
    q2_all_collabs = (
        df_collaborators
        .groupby(['collaborator_id', 'collaborator_name', 'collaborator_type'])
        .size().reset_index(name='work_count')
        .sort_values('work_count', ascending=False)
        .reset_index(drop=True)
    )
    q2_all_collabs['genre'] = q2_all_collabs['collaborator_id'].map(_id_to_genre).fillna('Unknown')

    # All hop1_from artists (directly influenced by Sailor)
    q2_all_hop1 = (
        df_influence_artists[df_influence_artists['direction'] == 'from_sailor']
        [['artist_id']].drop_duplicates().dropna(subset=['artist_id']).reset_index(drop=True)
    )
    q2_all_hop1['artist_name'] = q2_all_hop1['artist_id'].map(id_to_name)
    q2_all_hop1['genre'] = q2_all_hop1['artist_id'].map(_id_to_genre).fillna('Unknown')

    # All hop2 bridges keyed by hop1_artist_id
    _b = df_bridges.copy()
    _b['hop2_name'] = _b['hop2_artist_id'].map(id_to_name)
    _b = _b.dropna(subset=['hop2_name'])
    q2_hop2_bridges = (
        _b
        .sort_values(['hop1_artist_id', 'hop2_name'])
        .reset_index(drop=True)
    )
    return q2_all_collabs, q2_all_hop1, q2_hop2_bridges


@app.cell
def _(mo, q2_all_hop1):
    # Q1B — UI controls
    # Dropdown lists all hop1 artists so any can be selected for hop-2 expansion
    q2_none_opt = '— Select an artist to reveal their connections —'
    q2_radial_select = mo.ui.dropdown(
        options=[q2_none_opt] + q2_all_hop1['artist_name'].tolist(),
        value=q2_none_opt,
        label='Expand the influence chain for:',
    )
    return q2_none_opt, q2_radial_select


@app.cell
def _(
    alt,
    background,
    node_color,
    nx,
    pd,
    q1_sailor_id,
    q1_sailor_name,
    q2_all_collabs,
    q2_all_hop1,
    q2_hop2_bridges,
    q2_none_opt,
    q2_radial_select,
    title,
):
    # Q1B — Node-link network

    _collabs = q2_all_collabs
    _hop1    = q2_all_hop1

    # Resolve dropdown selection
    _sel_name = q2_radial_select.value
    _sel_aid  = None
    if _sel_name != q2_none_opt:
        _m = _hop1[_hop1['artist_name'] == _sel_name]
        if not _m.empty:
            _sel_aid = int(_m.iloc[0]['artist_id'])

    # Hop-2 subset (only when an artist is selected)
    _hop2 = pd.DataFrame()
    if _sel_aid is not None:
        _hop2 = q2_hop2_bridges[
            q2_hop2_bridges['hop1_artist_id'] == _sel_aid
        ].reset_index(drop=True)

    # Build network graph
    _G = nx.Graph()
    _G.add_node(
        q1_sailor_id,
        label=q1_sailor_name,
        node_type='Sailor',
        genre=None,
        size=300,
    )

    for _, _r in _collabs.iterrows():
        _nid = f"c_{_r['collaborator_id']}"
        _G.add_node(
            _nid,
            label=_r['collaborator_name'],
            node_type='Collaborator',
            genre=_r['genre'],
            size=max(50, min(250, int(_r['work_count']) * 15)),
        )
        _G.add_edge(q1_sailor_id, _nid)

    for _, _r in _hop1.iterrows():
        _nid = f"h1_{_r['artist_id']}"
        _G.add_node(
            _nid,
            label=_r['artist_name'],
            node_type='Directly influenced',
            genre=_r['genre'],
            size=60,
        )
        _G.add_edge(q1_sailor_id, _nid)

    for _, _r in _hop2.iterrows():
        _h1_nid = f"h1_{_sel_aid}"
        _h2_nid = f"h2_{_r['hop2_artist_id']}"
        _G.add_node(
            _h2_nid,
            label=_r['hop2_name'],
            node_type='Indirectly influenced',
            genre=_r['hop2_genre'],
            size=60,
        )
        if _G.has_node(_h1_nid):
            _G.add_edge(_h1_nid, _h2_nid)

    # Ring layout 
    _shell_inner = (
        [f"c_{r['collaborator_id']}" for _, r in _collabs.iterrows()] +
        [f"h1_{r['artist_id']}" for _, r in _hop1.iterrows()]
    )
    _shell_inner = [n for n in _shell_inner if _G.has_node(n)]
    _shell_outer = [
        f"h2_{r['hop2_artist_id']}" for _, r in _hop2.iterrows()
        if _G.has_node(f"h2_{r['hop2_artist_id']}")
    ]
    _shells = [[q1_sailor_id], _shell_inner] + ([_shell_outer] if _shell_outer else [])
    _pos = nx.shell_layout(_G, nlist=_shells)

    # Node dataframe
    _node_rows = [
        {
            'node_id': _nid,
            'x': float(_pos[_nid][0]),
            'y': float(_pos[_nid][1]),
            'label': _data['label'],
            'node_type': _data['node_type'],
            'genre': _data['genre'],
            'size': _data['size'],
        }
        for _nid, _data in _G.nodes(data=True)
    ]
    _nodes_df = pd.DataFrame(_node_rows)
    _nodes_df["genre"] = _nodes_df["genre"].fillna("Unknown")
    _nodes_df["size"]  = _nodes_df["size"].fillna(50)

    # Edge dataframe
    _edge_rows = [
        {
            'x': float(_pos[_u][0]), 'y': float(_pos[_u][1]),
            'x2': float(_pos[_v][0]), 'y2': float(_pos[_v][1]),
        }
        for _u, _v in _G.edges()
    ]
    _edges_df = (
        pd.DataFrame(_edge_rows)
        if _edge_rows
        else pd.DataFrame(columns=['x', 'y', 'x2', 'y2'])
    )

    _color_scale = alt.Scale(
        domain=list(node_color.keys()),
        range=list(node_color.values()),
    )

    _zoom = alt.selection_interval(bind='scales')

    _edges_layer = (
        alt.Chart(_edges_df)
        .mark_rule(strokeWidth=0.8, color='#d0dce8', opacity=0.8)
        .encode(
            x=alt.X('x:Q', axis=None),
            y=alt.Y('y:Q', axis=None),
            x2='x2:Q',
            y2='y2:Q',
        )
    )

    _nodes_layer = (
        alt.Chart(_nodes_df)
        .mark_circle(stroke='#1a2d3e', strokeWidth=0.6, opacity=0.9)
        .encode(
            x=alt.X('x:Q', axis=None),
            y=alt.Y('y:Q', axis=None),
            color=alt.Color(
                'node_type:N',
                scale=_color_scale,
                legend=alt.Legend(title='Node type', orient='right'),
            ),
            size=alt.Size('size:Q', scale=alt.Scale(range=[30, 500]), legend=None),
            tooltip=[
                alt.Tooltip('label:N',     title='Name'),
                alt.Tooltip('node_type:N', title='Type'),
                alt.Tooltip('genre:N',     title='Genre'),
            ],
        )
        .add_params(_zoom)
    )

    # Label only Sailor Shift at the centre
    _sailor_df = _nodes_df[_nodes_df['node_type'] == 'Sailor']
    _labels_layer = (
        alt.Chart(_sailor_df)
        .mark_text(dy=-14, fontSize=11, fontWeight='bold', color=title)
        .encode(
            x=alt.X('x:Q', axis=None),
            y=alt.Y('y:Q', axis=None),
            text='label:N',
        )
    )

    _fig = (
        alt.layer(_edges_layer, _nodes_layer, _labels_layer)
        .properties(
            width=680,
            height=540,
            title=alt.TitleParams(
                'Q1B — Who Has Sailor Shift Collaborated With And Directly Or Indirectly Influenced?',
                color=title,
                subtitleColor=title,
                fontSize=14,
                subtitleFontSize=11,
            ),
        )
        .configure_view(strokeWidth=0)
        .configure(background=background)
    )

    q2_radial_view = _fig
    return (q2_radial_view,)


@app.cell
def _(df_collaborators, df_of_yearly):
    # Q1C — pre-compute stacked area data
    _collab_ids = set(df_collaborators['collaborator_id'])

    # Sailor was not active until 2023 so no influence until then
    def _status(row):
        if row['release_year'] < 2023: return 'No influence'
        if row['influenced_by_sailor']: return 'Influenced by Sailor'
        if row['artist_id'] in _collab_ids: return 'Collaborator of Sailor'
        return 'No influence'

    _q3_base = df_of_yearly.copy()
    _q3_base['influence_status'] = _q3_base.apply(_status, axis=1)

    # Aggregate to (year, group) totals — one row per year per category
    q3_sg_data = (
        _q3_base
        .groupby(['release_year', 'influence_status'])['yearly_count']
        .sum()
        .reset_index()
    )

    # Stack order
    _sort_order = {'No influence': 0, 'Collaborator of Sailor': 1, 'Influenced by Sailor': 2}
    q3_sg_data['sort_order'] = q3_sg_data['influence_status'].map(_sort_order)

    q3_status_order = ['No influence', 'Collaborator of Sailor', 'Influenced by Sailor']
    q3_status_colors = ['#aed4e6', '#4ece99', '#3e9acb']
    return q3_sg_data, q3_status_colors, q3_status_order


@app.cell
def _(
    alt,
    background,
    q3_sg_data,
    q3_status_colors,
    q3_status_order,
    tick,
    title,
):
    # Q1C — Stacked Area Chart: how has Sailor influenced the broader Oceanus Folk community?

    q3_sg = (
        alt.Chart(q3_sg_data)
        .mark_area(interpolate='monotone', opacity=0.85)
        .encode(
            x=alt.X('release_year:Q',
                    axis=alt.Axis(title='Year', grid=False, format='d',
                                  labelColor=title, titleColor=title, tickColor=tick,
                                  labelFontSize=12, titleFontSize=13)),
            y=alt.Y('yearly_count:Q',
                    stack=True,
                    axis=alt.Axis(title='Oceanus Folk works released', labelColor=title,
                                  titleColor=title, tickColor=tick, grid=False)),
            color=alt.Color('influence_status:N',
                            scale=alt.Scale(domain=q3_status_order, range=q3_status_colors),
                            legend=alt.Legend(title='Relationship to Sailor',
                                             labelColor=title, titleColor=title, orient='right')),
            order=alt.Order('sort_order:Q', sort='ascending'),
            tooltip=[
                alt.Tooltip('influence_status:N', title='Group'),
                alt.Tooltip('release_year:Q', title='Year', format='d'),
                alt.Tooltip('yearly_count:Q', title='OF works released'),
            ]
        )
        .properties(
            width=640, height=400,
            title=alt.TitleParams(
                'Q3 — How Has Sailor Shift Influenced Collaborators of the Broader Oceanus Folk Community?',
                color=title, fontSize=14, fontWeight='bold'
            )
        )
    )

    q3_area_view = (
        q3_sg
        .configure_view(fill=background, stroke=None, strokeWidth=0)
        .configure(background=background)
    )
    return (q3_area_view,)


@app.cell
def _(mo, q1_bar, q1_sg_view, q2_radial_select, q2_radial_view, q3_area_view):
    #_row1 = mo.hstack([q1_sg_view, q1_bar], gap=2)
    _score_key = mo.md("**Score:** 5 = DirectlySamples · 4 = CoverOf · 3 = InterpolatesFrom · 2 = LyricalReferenceTo · 1 = InStyleOf")
    _q1_bar_panel = mo.vstack([q1_bar, _score_key])
    _row1 = mo.hstack([q1_sg_view, _q1_bar_panel], gap=2)

    _q2_panel = mo.vstack([q2_radial_select, q2_radial_view])
    _row2 = mo.hstack([_q2_panel, q3_area_view], gap=2)

    mo.vstack([_row1,_row2])
    return


@app.cell
def _(mo):
    mo.md(r"""
    # Q2

    This section implements the analysis of **Question 2**, by constructing a pipeline that traces how **Oceanus Folk** songs influence other songs, genres, and artists over time. The process begins with data preprocessing and the extraction of influenced songs based on multiple relationship fields, followed by the creation of aggregated datasets for temporal and categorical analysis. These are visualized using an interactive trend chart, heatmap, and lollipop chart, which together provide insights into the evolution, spread, and key contributors of Oceanus Folk influence. Finally, these components are integrated into a single interactive dashboard.
    """)
    return


@app.cell
def _(df_persons):
    # filters the df_persons dataset to identify rows corresponding to the artist Sailor
    # ensures case insensitive matching 
    # prevents errors if there are missing values in the "name" column
    df_persons[df_persons["name"].str.contains("Sailor", case=False, na=False)]
    return


@app.cell
def _(df_persons):
    # storeS the filtered result for reuse
    q2a_sailor_row = df_persons[df_persons["name"].str.contains("Sailor", case=False, na=False)]
    return (q2a_sailor_row,)


@app.cell
def _(q2a_sailor_row):
    # extracts the id of the first matching row (assumes Sailor appears at least once)
    q2a_sailor_id = q2a_sailor_row.iloc[0]["id"]

    # extracts the name of the artist for reference and validation
    q2a_sailor_name = q2a_sailor_row.iloc[0]["name"]
    return


@app.function
# standardizes inconsistent data formats, converts lists stored as strings into python proper lists and also handles missing values
def q2a_parse_list_field(x):
    import ast
    import pandas as pd

    # if already a list, return as is
    if isinstance(x, list):
        return x

    # handle None values
    if x is None:
        return []

    # handle None values
    if isinstance(x, float) and pd.isna(x):
        return []

    # if value is a string, attempt to parse it as a Python list
    if isinstance(x, str):
        try:
            parsed = ast.literal_eval(x)

            # if parsing succeeds and returns a list, then use it
            # otherwise wrap single values into a list
            return parsed if isinstance(parsed, list) else [parsed]

        # if parsing fails, return the original string inside a list
        except Exception:
            return [x]
    return []


@app.function
# counts how frequently each artist appears in a given column and returns the top 10 most frequent artists
def q2a_count_artists_from_column(df, col="performed_by_persons", top_n=10):
    from collections import Counter
    import pandas as pd

    counter = Counter()
    # iterates through all non missing entries in the column
    for artists in df[col].dropna():

        # parses each entry into a proper list
        counter.update(q2a_parse_list_field(artists))

    # convert counts into a dataframe for easier sorting and visualization
    return (
        pd.DataFrame(counter.items(), columns=["artist", "count"])
        .sort_values("count", ascending=False) # highest counts first
        .head(top_n) # keep only top N artists
    )


@app.function
# constructs a time based aggregation of songs by year for temporal trend analysis
def q2a_build_genre_trend(df):
    import pandas as pd
    # creates a copy to avoid modifying the original dataframe
    temp = df.copy()
    # converts date column to datetime and extracts the year
    temp["year"] = pd.to_datetime(
        temp["date"], errors="coerce" # ensures invalid dates become NaT instead of crashing
    ).dt.year

    # remove rows without a valid year
    # then group by year and count number of songs per year
    return (
        temp.dropna(subset=["release_year"])
        .groupby("release_year")
        .size()
        .reset_index(name="count")
    )


@app.cell
def _(df_song_edges):
    # getting oceanus folk songs
    # basis for analyzing influence spread
    q2a_oceanus_df = df_song_edges[
        df_song_edges["genre"].str.contains("Oceanus Folk", case=False, na=False)
    ].copy()
    return (q2a_oceanus_df,)


@app.function
# finding songs influenced by Oceanus Folk
# scans multiple relationship columns and collects the unique song names that appear as influence targets
def q2a_extract_all_influenced_songs(df):
    import itertools
    # relationship columns that may contain songs influenced by the source songs
    cols = [
        "in_style_of_songs",
        "interpolates_from_songs",
        "cover_of_songs",
        "directly_samples_songs"
    ]

    all_targets = []

    # loops through each relationship column and extracts song names
    for col in cols:
        for x in df[col].dropna():
            all_targets.extend(q2a_parse_list_field(x))

    return list(set(all_targets))


@app.cell
def _(q2a_oceanus_df):
    # applying the helper function to the Oceanus Folk subset to create a unique list of song names influenced by Oceanus Folk songs
    influenced_song_names = q2a_extract_all_influenced_songs(q2a_oceanus_df)
    return


@app.cell
def _(df_song_edges, pd):
    # allows extraction of targets from any set of columns
    # a more reusable function for influence extraction
    def q2a_extract_targets_from_cols(df, cols):
        targets = []
        for col in cols:
            # skip the column if it is not present in the dataframe
            if col not in df.columns:
                continue

            # parse each non missing value and extend the target list
            for x in df[col].dropna():
                targets.extend(q2a_parse_list_field(x))
        return list(set(targets)) # return unique targets only

    # this builds the 'influenced' dataset
    # starts from oceanus folk songs, finds all songs influenced by them, filters the dataset to include only those influenced songs and their release year
    def q2a_build_oceanus_influenced_df():
        # source songs in Oceanus Folk
        q2a_oceanus_df = df_song_edges[
            df_song_edges["genre"].str.contains("Oceanus Folk", case=False, na=False)
        ].copy()

        influence_song_cols = [
            "in_style_of_songs",
            "interpolates_from_songs",
            "cover_of_songs",
            "directly_samples_songs",
            "lyrical_ref_to_songs",
        ]

        # extracts all unique influenced song names from the selected columns
        influenced_song_names = q2a_extract_targets_from_cols(q2a_oceanus_df, influence_song_cols)

        # keeps only rows from the full dataset that match the influenced song names
        q2a_influenced_df = df_song_edges[
            df_song_edges["name"].isin(influenced_song_names)
        ].copy()

        # converts release_date into a datetime variable and extracts only the year
        # this will help the later on yearly trend analysis and dashboard filtering
        q2a_influenced_df["year"] = pd.to_datetime(
            q2a_influenced_df["release_date"], errors="coerce"
        ).dt.year

        return q2a_influenced_df
    return (q2a_build_oceanus_influenced_df,)


@app.cell
def _(q2a_build_oceanus_influenced_df):
    # the final influenced songs dataset used in the dashboard
    q2a_influenced_df = q2a_build_oceanus_influenced_df()
    #q2a_influenced_df.head()
    return (q2a_influenced_df,)


@app.cell
def _(mo, q2a_influenced_df):
    # extracts only valid year values for slider setup
    # missing years are removed and the remaining values are converted to integers
    valid_years = q2a_influenced_df["year"].dropna().astype(int)
    # min and max year available in the dataset
    min_year = int(valid_years.min())
    max_year = int(valid_years.max())

    # year slider to filter the dataset by a selected year range
    q2a_year_slider = mo.ui.range_slider(
        start=min_year,
        stop=max_year,
        value=[min_year, max_year],
        label="Select Year Range"
    )
    return (q2a_year_slider,)


@app.cell
def _(q2a_influenced_df, q2a_year_slider):
    # in this cell, the selected year range is applied to filter the dataset
    start_year, end_year = q2a_year_slider.value

    # keeps only influenced songs whose release year falls within the selected range
    q2a_filtered_influenced_df = q2a_influenced_df[
        q2a_influenced_df["year"].between(start_year, end_year)
    ].copy()

    # aggregates the nr of influenced songs per year ( basis for time series visualization)
    q2a_trend_df = (
        q2a_filtered_influenced_df
        .dropna(subset=["year"])
        .groupby("year")
        .size()
        .reset_index(name="count")
    )

    # most frequent genres amongst influenced songs, to see which genres were most influenced by Oceanus Folk
    top_genres_df = (
        q2a_filtered_influenced_df["genre"]
        .dropna()
        .value_counts()
        .reset_index()
    )
    top_genres_df.columns = ["genre", "count"]
    top_genres_df = top_genres_df.head(12) # keeps only the top 12 genres

    # stores the selected genre names in a list for filtering
    top_genre_names = top_genres_df["genre"].tolist()

    # creates a dataset to show how genre influence changes over time , used for the heatmap later
    q2a_genre_year_df = (
        q2a_filtered_influenced_df[
            q2a_filtered_influenced_df["genre"].isin(top_genre_names)
        ]
        .dropna(subset=["genre", "year"])
        .groupby(["genre", "year"])
        .size()
        .reset_index(name="count")
    )

    # most influential artists based on how often the appear in influenced songs
    top_artists_df = q2a_count_artists_from_column(
        q2a_filtered_influenced_df,
        col="performed_by_persons",
        top_n=15
    )

    #q2a_trend_df.head(), q2a_genre_year_df.head(), top_artists_df.head()
    return q2a_filtered_influenced_df, q2a_genre_year_df, q2a_trend_df


@app.cell
def _(
    alt,
    mo,
    q2a_filtered_influenced_df,
    q2a_genre_year_df,
    q2a_trend_df,
    q2a_year_slider,
):

    # allows users to filter and highlight data by genre
    genre_select = alt.selection_point(fields=["genre"], empty=True)

    # trend chart
    # Base chart shared by the trend layers
    trend_base = alt.Chart(q2a_trend_df).encode(
        x=alt.X("year:Q", title="Year", axis=alt.Axis(format="d", tickMinStep=1)),
        y=alt.Y("count:Q", title="Number of Influenced Songs"),
    )

    # Adds a filled background under the line to emphasize overall magnitude
    # opacity is  low so the chart does not become too heavy
    # line=True also draws an outline around the area
    trend_area = trend_base.mark_area(
        opacity=0.28,
        line=True
    ).encode(
        tooltip=[
            alt.Tooltip("year:Q", title="Year", format="d"),
            alt.Tooltip("count:Q", title="Influenced Songs")
        ]
    )

    # Main line layer used to show the continuous evolution of influence over time
    trend_line = trend_base.mark_line(
        strokeWidth=3
    )

    # Point layer that adds visible circles for each yearly observation (makes it easier to identify exact values)
    trend_points = trend_base.mark_circle(
        size=70,
        opacity=0.95
    )

    # Rolling average preparation:
    # made a copy of the dataframe so the original stays unchanged
    # The rolling average smooths short-term fluctuations (3 year window)
    # helps reveal the broader pattern over time
    rolling_df = q2a_trend_df.copy()
    # min_periods=1 ensures the first years are still calculated even though there are not yet 3 earlier values available
    rolling_df["rolling_avg"] = rolling_df["count"].rolling(3, min_periods=1).mean()

    # Rolling average line:
    # This line is visually differentiated from the main trend using a dashed pattern
    # It helps compare yearly volatility with smoothed long term tendency
    rolling_line = alt.Chart(rolling_df).mark_line(
        strokeDash=[6, 4],
        strokeWidth=2
    ).encode(
        x=alt.X("year:Q", axis=alt.Axis(format="d", tickMinStep=1)),
        y=alt.Y("rolling_avg:Q"),
        tooltip=[
            alt.Tooltip("year:Q", title="Year", format="d"),
            alt.Tooltip("rolling_avg:Q", title="3-Year Rolling Avg", format=".2f")
        ]
    )

    # Adds a horizontal dashed line at the mean count across all years to give a benchmark for seeing which periods are above or below average
    peak_rule = alt.Chart(q2a_trend_df).mark_rule(strokeDash=[2, 2], opacity=0.45).encode(
        y="mean(count):Q"
    )

    # Final trend chart:
    # All layers are combined into one chart and the width is kept large because this is the main temporal overview in the dashboard..
    trend_chart = (
        (trend_area + trend_line + trend_points + rolling_line + peak_rule)
        .properties(
            title="Spread of Oceanus Folk Influence Over Time",
            width=1000,
            height=360
        )
    )

    # heatmap that shows which genres were most influenced across different years
    # gives a compact overview of how influence spreads across genres over time
    heatmap = (
        alt.Chart(q2a_genre_year_df)
        .mark_rect()  # each rectangle represents a year/genre combination
        .encode(
            x=alt.X("year:O", title="Year"), # x-axis = year, treated as ordinal so every year gets one distinct column
            y=alt.Y("genre:N", sort="-x", title="Influenced Genre"), # sort="-x" sorts genres by count descending based on encoding context
            # color intensity represents number of influenced songs ( darker = higher influence)
            color=alt.Color(
                "count:Q",
                title="Influence Count",
                scale=alt.Scale(scheme="tealblues")
            ),
            # tooltips allow exact inspection of each cell
            tooltip=[
                alt.Tooltip("genre:N", title="Genre"),
                alt.Tooltip("year:O", title="Year"),
                alt.Tooltip("count:Q", title="Influence Count")
            ],
            opacity=alt.condition(genre_select, alt.value(1), alt.value(0.88))
        )
        .add_params(genre_select) # adds the interactive selection parameter to this chart
        .properties(
            title="Influenced Genres Across Time",
            width=560,
            height=360
        )
    )

    # lollipop chart that shows which artists appear most frequently among the influenced songs
    # starts from the filtered influenced songs dataframe

    # This dataframe already reflects the selected year range
    artist_source_df = q2a_filtered_influenced_df.copy()
    # The performed_by_persons column stores artists in a list like format and q2a_parse_list_field converts those entries into Python lists
    artist_source_df["performed_by_persons_clean"] = artist_source_df["performed_by_persons"].apply(q2a_parse_list_field)

    # explode() turns each list of artists into separate rows, so each artist gets counted individually
    # rename() makes the column easier to work with
    artist_source_df = artist_source_df.explode("performed_by_persons_clean").rename(
        columns={"performed_by_persons_clean": "artist"}
    )

    # Removes rows where artist information is missing
    artist_source_df = artist_source_df.dropna(subset=["artist"])

    # Counts how often each artist appears in the influenced songs
    # Then sort descending and keep only the top 15 artists
    top_artists_plot_df = (
        artist_source_df.groupby("artist")
        .size()
        .reset_index(name="count")
        .sort_values("count", ascending=False)
        .head(15)
    )

    # Base chart for reuse in the lollipop layers
    base = alt.Chart(top_artists_plot_df)

    # These are the horizontal lines that run from zero to the artist's count (the "stick" part of the lollipop)
    lollipop_lines = base.mark_rule(strokeWidth=2).encode(
        x=alt.X("count:Q", title="Influence Count"),
        y=alt.Y("artist:N", sort="-x", title="Artist")
    )

    # These mark the endpoint of each line
    # Color intensity is also mapped to count for additional emphasis
    lollipop_points = base.mark_circle(size=120).encode(
        x=alt.X("count:Q"),
        y=alt.Y("artist:N", sort="-x"),
        color=alt.Color("count:Q", scale=alt.Scale(scheme="blues"), legend=None),
        tooltip=[
            alt.Tooltip("artist:N", title="Artist"),
            alt.Tooltip("count:Q", title="Influence Count")
        ]
    )

    # Text labels that display the exact count next to each circle so the viewer does not need to rely only on axis reading or tooltip hovering
    artist_labels = base.mark_text(
        align="left",
        dx=8, # slight horizontal offset so text does not overlap the point
        fontSize=11
    ).encode(
        x=alt.X("count:Q"),
        y=alt.Y("artist:N", sort="-x"),
        text=alt.Text("count:Q")
    )

    # Final lollipop chart that combines the lines, points, and value labels
    artists_chart = (
        lollipop_lines + lollipop_points + artist_labels
    ).properties(
        title="Top Influenced Artists",
        width=430,
        height=360
    )

    # Final dashboard layout that:
    # Combines all visual components into one vertical dashboard view
    # mo.vstack() stacks components from top to bottom in a readable order
    # The slider is placed near the top because it controls the filtered dataset used by the charts below

    mo.vstack([
        mo.md("## Oceanus Folk Influence Dashboard"),
        q2a_year_slider, # interactive year range control
        mo.md("### Trends Over Time"),  # temporal spread of influence
        trend_chart,
        mo.md("### Genre Heatmap"), # cross-genre spread over time
        heatmap,
        mo.md("### Top Artists"), # most frequently appearing artists in influenced songs
        artists_chart,
    ])
    return


@app.cell
def _(mo):
    mo.md(r"""
    # Q3
    Use your visualizations to develop a profile of what it means to be a rising star in the music industry.

    **a) Visualize the careers of three artists. Compare and contrast their rise in popularity and influence.**

    Line graphs for time series (real + cohort) analysis on releases and influences
    Bar charts to compare distributions among fields like release type, influence type, genre, project role, and aggregated fields that are min-max normalized among the dataset, such as:

    - notable_rate: notable releases / total releases
    - performance: notable releases / years active
    - influence_efficiency: total influenced works / total releases
    - breakout_delay: years between debut and first influence

    **b) Using this characterization, give three predictions of who the next Oceanus Folk stars with be over the next five years**
    Scatterplot of a set of artists and groups that are filtered out on the table, showing the differences in number of releases, years of activity, and notable rate. The genre filter is applied based on the most frequent genre among the discography of an artist.
    """)
    return


@app.cell
def _(df_all_edges, df_all_nodes, pd):
    # ── Flat influence edge table — ID-based, captures all type combinations ──
    _INFLUENCE_TYPES = {
        "InStyleOf", "InterpolatesFrom", "CoverOf",
        "DirectlySamples", "LyricalReferenceTo",
    }
    # year from source node release_date (works for songs, albums, persons, groups)
    _year_lookup = (
        df_all_nodes.set_index("id")["release_date"]
        .str[:4]
        .apply(pd.to_numeric, errors="coerce")
        .dropna()
        .astype(int)
        .to_dict()
    )
    q3_df_influence_edges = (
        df_all_edges[df_all_edges["Edge Type"].isin(_INFLUENCE_TYPES)]
        .copy()
        .rename(columns={"Edge Type": "edge_type"})
        [["source", "source_name", "source_type",
          "target", "target_name", "target_type",
          "edge_type"]]
        .reset_index(drop=True)
    )
    q3_df_influence_edges["year"] = q3_df_influence_edges["source"].map(_year_lookup)

    print(f"q3_df_influence_edges: {q3_df_influence_edges.shape}")
    print(f"\nEdge type counts:")
    print(q3_df_influence_edges["edge_type"].value_counts().to_string())
    print(f"\nSource → Target type pairs:")
    print(
        q3_df_influence_edges
        .groupby(["source_type", "target_type"])
        .size()
        .rename("count")
        .reset_index()
        .sort_values("count", ascending=False)
        .to_string(index=False)
    )
    # q3_df_influence_edges
    return (q3_df_influence_edges,)


@app.cell
def _(
    df_album_edges,
    df_all_nodes,
    df_group_edges,
    df_person_edges,
    df_song_edges,
    pd,
    q3_df_influence_edges,
):
    # Compute career metrics (notable rate, influence efficiency, breakout delay) for all persons and groups
    _notable_songs  = set(df_song_edges[df_song_edges["notable"] == True]["name"])
    _notable_albums = set(df_album_edges[df_album_edges["notable"] == True]["name"])

    _song_role_cols  = ["performer_of_songs",  "composer_of_songs",  "producer_of_songs",  "lyricist_of_songs"]
    _album_role_cols = ["performer_of_albums", "composer_of_albums", "producer_of_albums", "lyricist_of_albums"]

    # release year lookups
    _song_year  = pd.to_datetime(df_song_edges["release_date"],  errors="coerce").dt.year.set_axis(df_song_edges["name"]).dropna().astype(int).to_dict()
    _album_year = pd.to_datetime(df_album_edges["release_date"], errors="coerce").dt.year.set_axis(df_album_edges["name"]).dropna().astype(int).to_dict()

    # genre lookups
    _song_genre  = df_song_edges.set_index("name")["genre"].dropna().to_dict()
    _album_genre = df_album_edges.set_index("name")["genre"].dropna().to_dict()

    # group → songs/albums performed
    _group_song_map, _group_album_map = {}, {}
    for _, _gr in df_group_edges.iterrows():
        _group_song_map[_gr["name"]]  = set(_gr["performer_of_songs"])  if isinstance(_gr.get("performer_of_songs"),  list) else set()
        _group_album_map[_gr["name"]] = set(_gr["performer_of_albums"]) if isinstance(_gr.get("performer_of_albums"), list) else set()

    # name → node ID lookup (used for ID-based influence queries)
    _name_to_id = {}
    for _nid, _nm in zip(df_all_nodes["id"], df_all_nodes["name"]):
        _name_to_id.setdefault(_nm, set()).add(_nid)

    _rows = []
    for _, _r in df_person_edges.iterrows():
        _pname  = _r["name"]
        _groups = _r.get("member_of") or []
        if not isinstance(_groups, list):
            _groups = []

        # own works (person roles + group performer roles)
        _songs, _albums = set(), set()
        for _col in _song_role_cols:
            if isinstance(_r.get(_col), list):
                _songs.update(_r[_col])
        for _col in _album_role_cols:
            if isinstance(_r.get(_col), list):
                _albums.update(_r[_col])
        for _grp in _groups:
            _songs.update(_group_song_map.get(_grp, set()))
            _albums.update(_group_album_map.get(_grp, set()))

        # release year span
        _years = [_song_year[s] for s in _songs if s in _song_year] + \
                 [_album_year[a] for a in _albums if a in _album_year]
        _first_yr = min(_years) if _years else None
        _last_yr  = max(_years) if _years else None
        _n_years_active = max((_last_yr - _first_yr), 1) if _first_yr and _last_yr else 1
        _n_releases = len(_songs) + len(_albums)

        # ── ID-based influence count ──────────────────────────────────────────
        _target_ids = set()
        for _nm in (_songs | _albums):
            _target_ids.update(_name_to_id.get(_nm, set()))
        _target_ids.add(_r["id"])          # use this person's actual ID — avoids merging same-name people
        for _nm in set(_groups):           # groups still resolved by name
            _target_ids.update(_name_to_id.get(_nm, set()))

        _hits = q3_df_influence_edges[
            q3_df_influence_edges["target"].isin(_target_ids) &
            ~q3_df_influence_edges["source"].isin(_target_ids)
        ]
        _src_counts = _hits["source_type"].value_counts()

        _n_songs_inf   = int(_src_counts.get("Song",         0))
        _n_albums_inf  = int(_src_counts.get("Album",        0))
        _n_persons_inf = int(_src_counts.get("Person",       0))
        _n_groups_inf  = int(_src_counts.get("MusicalGroup", 0))
        _total_inf     = int(_src_counts.sum())

        _inf_years = _hits["year"].dropna()

        # most worked genre: mode across all songs + albums
        _genres = (
            [_song_genre[s]  for s in _songs  if s in _song_genre] +
            [_album_genre[a] for a in _albums if a in _album_genre]
        )
        _genre_series = pd.Series(_genres)
        _most_genre = _genre_series.mode().iloc[0] if not _genre_series.empty else None

        _rows.append({
            "person_id":                     _r["id"],
            "person":                        _pname,
            "entity_type":                   "Person",
            "groups":                        ", ".join(_groups) if _groups else None,
            "number_songs_collaborated":     len(_songs),
            "number_albums_collaborated":    len(_albums),
            "number_songs_notable":          len(_songs  & _notable_songs),
            "number_albums_notable":         len(_albums & _notable_albums),
            "songs_influenced_by_artist":    _n_songs_inf,
            "albums_influenced_by_artist":   _n_albums_inf,
            "persons_influenced_by_artist":  _n_persons_inf,
            "groups_influenced_by_artist":   _n_groups_inf,
            "total_influenced":              _total_inf,
            "first_release_year":            _first_yr,
            "last_release_year":             _last_yr,
            "n_years_active":                _n_years_active,
            "first_influence_year":          int(_inf_years.min()) if not _inf_years.empty else None,
            "most_worked_genre":             _most_genre,
        })

    df_person_career = pd.DataFrame(_rows)

    df_person_career["total_releases"] = (
        df_person_career["number_songs_collaborated"] + df_person_career["number_albums_collaborated"]
    )
    df_person_career["breakout_delay"] = (
        df_person_career["first_influence_year"] - df_person_career["first_release_year"]
    )
    _tr = df_person_career["total_releases"].where(df_person_career["total_releases"] > 0)
    _ya = df_person_career["n_years_active"].where(df_person_career["n_years_active"] > 0)
    df_person_career["influence_efficiency"] = df_person_career["total_influenced"] / _tr
    df_person_career["notable_rate"] = (
        (df_person_career["number_songs_notable"] + df_person_career["number_albums_notable"]) / _tr
    )
    df_person_career["performance"] = (
        (df_person_career["number_songs_notable"] + df_person_career["number_albums_notable"]) / _ya
    )
    df_person_career = (
        df_person_career
        .sort_values("total_influenced", ascending=False)
        .reset_index(drop=True)
    )
    print(f"df_person_career: {df_person_career.shape}")
    # df_person_career

    _g_notable_songs  = set(df_song_edges[df_song_edges["notable"] == True]["name"])
    _g_notable_albums = set(df_album_edges[df_album_edges["notable"] == True]["name"])
    _g_song_year  = pd.to_datetime(df_song_edges["release_date"], errors="coerce").dt.year.set_axis(df_song_edges["name"]).dropna().astype(int).to_dict()
    _g_album_year = pd.to_datetime(df_album_edges["release_date"], errors="coerce").dt.year.set_axis(df_album_edges["name"]).dropna().astype(int).to_dict()
    _g_song_genre  = df_song_edges.set_index("name")["genre"].dropna().to_dict()
    _g_album_genre = df_album_edges.set_index("name")["genre"].dropna().to_dict()
    _g_name_to_id = {}
    for _nid, _nm in zip(df_all_nodes["id"], df_all_nodes["name"]):
        _g_name_to_id.setdefault(_nm, set()).add(_nid)

    _g_rows = []
    for _, _r in df_group_edges.iterrows():
        _gname  = _r["name"]
        _songs  = set(_r["performer_of_songs"])  if isinstance(_r.get("performer_of_songs"),  list) else set()
        _albums = set(_r["performer_of_albums"]) if isinstance(_r.get("performer_of_albums"), list) else set()
        _years  = [_g_song_year[s] for s in _songs  if s in _g_song_year] + \
                  [_g_album_year[a] for a in _albums if a in _g_album_year]
        _first_yr = min(_years) if _years else None
        _last_yr  = max(_years) if _years else None
        _n_yrs    = max((_last_yr - _first_yr), 1) if _first_yr and _last_yr else 1
        _target_ids = set()
        for _w in (_songs | _albums):
            _target_ids.update(_g_name_to_id.get(_w, set()))
        _target_ids.update(_g_name_to_id.get(_gname, set()))
        _hits       = q3_df_influence_edges[q3_df_influence_edges["target"].isin(_target_ids) & ~q3_df_influence_edges["source"].isin(_target_ids)]
        _sc         = _hits["source_type"].value_counts()
        _inf_years  = _hits["year"].dropna()
        _genres     = [_g_song_genre[s] for s in _songs if s in _g_song_genre] + \
                      [_g_album_genre[a] for a in _albums if a in _g_album_genre]
        _gs         = pd.Series(_genres)
        _g_rows.append({
            "person_id":                     _r["id"],
            "person":                        _gname,
            "entity_type":                   "Group",
            "groups":                        None,
            "number_songs_collaborated":     len(_songs),
            "number_albums_collaborated":    len(_albums),
            "number_songs_notable":          len(_songs  & _g_notable_songs),
            "number_albums_notable":         len(_albums & _g_notable_albums),
            "songs_influenced_by_artist":    int(_sc.get("Song",         0)),
            "albums_influenced_by_artist":   int(_sc.get("Album",        0)),
            "persons_influenced_by_artist":  int(_sc.get("Person",       0)),
            "groups_influenced_by_artist":   int(_sc.get("MusicalGroup", 0)),
            "total_influenced":              int(_sc.sum()),
            "first_release_year":            _first_yr,
            "last_release_year":             _last_yr,
            "n_years_active":                _n_yrs,
            "first_influence_year":          int(_inf_years.min()) if not _inf_years.empty else None,
            "most_worked_genre":             _gs.mode().iloc[0] if not _gs.empty else None,
        })

    df_group_career = pd.DataFrame(_g_rows)
    if not df_group_career.empty:
        _tr  = df_group_career["number_songs_collaborated"] + df_group_career["number_albums_collaborated"]
        _trw = _tr.where(_tr > 0)
        _yaw = df_group_career["n_years_active"].where(df_group_career["n_years_active"] > 0)
        df_group_career["total_releases"]       = _tr
        df_group_career["notable_releases"]     = df_group_career["number_songs_notable"] + df_group_career["number_albums_notable"]
        df_group_career["notable_rate"]         = df_group_career["notable_releases"] / _trw
        df_group_career["performance"]          = df_group_career["notable_releases"] / _yaw
        df_group_career["influence_efficiency"] = df_group_career["total_influenced"]  / _trw
        df_group_career["breakout_delay"]       = df_group_career["first_influence_year"] - df_group_career["first_release_year"]
    return df_group_career, df_person_career


@app.cell
def _(alt, df_person_career, mo, pd):
    # Population distribution charts: songs and albums collaborated count histograms
    def _hist_df(series, n_bins=40):
        series = series.dropna()
        bins = pd.cut(series, bins=n_bins)
        h = bins.value_counts().sort_index().reset_index()
        h.columns = ["bin", "count"]
        h["left"]  = h["bin"].apply(lambda x: x.left).astype(float)
        h["right"] = h["bin"].apply(lambda x: x.right).astype(float)
        return h[["left", "right", "count"]]

    def _dist_chart(hist, x_title, chart_title, width=400):
        return (
            alt.Chart(hist).mark_bar(color="#4C78A8")
            .encode(
                x=alt.X("left:Q",  title=x_title),
                x2="right:Q",
                y=alt.Y("count:Q", title="Artists"),
                tooltip=[
                    alt.Tooltip("left:Q",  title="From"),
                    alt.Tooltip("right:Q", title="To"),
                    alt.Tooltip("count:Q", title="Artists"),
                ],
            )
            .properties(title=chart_title, width=width, height=200)
        )

    _dist_songs  = _dist_chart(_hist_df(df_person_career["number_songs_collaborated"]),
                                "Songs Collaborated", "Songs Collaborated — full population", width=300)
    _dist_albums = _dist_chart(_hist_df(df_person_career["number_albums_collaborated"]),
                                "Albums Collaborated", "Albums Collaborated — full population", width=300)

    dist_charts_view = mo.ui.altair_chart(alt.hconcat(_dist_songs, _dist_albums))
    return (dist_charts_view,)


@app.cell
def _(df_person_career, mo):
    # Filter controls: sliders and dropdowns for the career explorer table
    _genres = ["(All)"] + sorted(df_person_career["most_worked_genre"].dropna().unique().tolist())

    min_songs    = mo.ui.slider(0, int(df_person_career["number_songs_collaborated"].max()),
                                value=0, step=1, label="Min songs")
    min_albums   = mo.ui.slider(0, int(df_person_career["number_albums_collaborated"].max()),
                                value=0, step=1, label="Min albums")
    _max_years   = int(df_person_career["n_years_active"].max())
    years_lo     = mo.ui.number(0, _max_years, value=0,          step=1, label="Min years active")
    years_hi     = mo.ui.number(0, _max_years, value=_max_years, step=1, label="Max years active")
    _min_yr      = int(df_person_career["last_release_year"].dropna().min())
    _max_yr      = int(df_person_career["last_release_year"].dropna().max())
    last_rel_lo  = mo.ui.number(_min_yr, _max_yr, value=_min_yr, step=1, label="Last release ≥")
    last_rel_hi  = mo.ui.number(_min_yr, _max_yr, value=_max_yr, step=1, label="Last release ≤")
    genre_filter = mo.ui.dropdown(_genres, value="(All)", label="Genre")
    role_filter  = mo.ui.dropdown(
        ["All", "Performer", "Composer", "Producer", "Lyricist"],
        value="All", label="Role",
    )
    release_type = mo.ui.dropdown(["All", "Song", "Album"], value="All", label="Release type")
    return (
        genre_filter,
        last_rel_hi,
        last_rel_lo,
        min_albums,
        min_songs,
        release_type,
        role_filter,
        years_hi,
        years_lo,
    )


@app.cell
def _(
    df_album_edges,
    df_group_career,
    df_person_career,
    df_person_edges,
    df_song_edges,
    genre_filter,
    last_rel_hi,
    last_rel_lo,
    min_albums,
    min_songs,
    pd,
    release_type,
    role_filter,
    years_hi,
    years_lo,
):
    # Apply filters to career table; also produce min-filtered subset for sub-metric profile
    _r = role_filter.value
    _t = release_type.value

    # ── Combine persons + groups ──────────────────────────────────────────────
    _combined_career = pd.concat([df_person_career, df_group_career], ignore_index=True)

    # ── Path A: no filters — use pre-computed table directly ──────────────────
    if _r == "All" and _t == "All":
        _base = _combined_career.assign(
            notable_releases=(_combined_career["number_songs_notable"]
                              + _combined_career["number_albums_notable"])
        )

    # ── Path B: role=All, type filtered — slice pre-computed columns ──────────
    elif _r == "All":
        _base = _combined_career.copy()
        if _t == "Song":
            _base["number_albums_collaborated"] = 0
            _base["total_releases"]   = _base["number_songs_collaborated"]
            _base["notable_releases"] = _base["number_songs_notable"]
        else:  # Album
            _base["number_songs_collaborated"] = 0
            _base["total_releases"]   = _base["number_albums_collaborated"]
            _base["notable_releases"] = _base["number_albums_notable"]
        _ya = _base["n_years_active"].where(_base["n_years_active"] > 0)
        _tr = _base["total_releases"].where(_base["total_releases"] > 0)
        _base["notable_rate"] = _base["notable_releases"] / _tr
        _base["performance"]  = _base["notable_releases"] / _ya

    # ── Path C: specific role — vectorised column-length operations ───────────
    else:
        _ns_set = set(df_song_edges [df_song_edges ["notable"] == True]["name"])
        _na_set = set(df_album_edges[df_album_edges["notable"] == True]["name"])

        _sc = {"Performer": "performer_of_songs",  "Composer": "composer_of_songs",
               "Producer":  "producer_of_songs",   "Lyricist": "lyricist_of_songs"}[_r]
        _ac = {"Performer": "performer_of_albums", "Composer": "composer_of_albums",
               "Producer":  "producer_of_albums",  "Lyricist": "lyricist_of_albums"}[_r]

        def _len(col):
            return col.apply(lambda x: len(x) if isinstance(x, list) else 0)
        def _notable(col, ns):
            return col.apply(lambda x: len(set(x) & ns) if isinstance(x, list) else 0)

        _zero = pd.Series(0, index=df_person_edges.index)
        _ns   = _len    (df_person_edges[_sc]) if _t != "Album" else _zero
        _nn_s = _notable(df_person_edges[_sc], _ns_set) if _t != "Album" else _zero
        _na   = _len    (df_person_edges[_ac]) if _t != "Song"  else _zero
        _nn_a = _notable(df_person_edges[_ac], _na_set) if _t != "Song"  else _zero

        _rc = pd.DataFrame({
            "person_id":                  df_person_edges["id"],
            "number_songs_collaborated":  _ns,
            "number_albums_collaborated": _na,
            "total_releases":             _ns + _na,
            "notable_releases":           _nn_s + _nn_a,
        })
        _persons_base = (
            df_person_career
            .drop(columns=["number_songs_collaborated", "number_albums_collaborated",
                            "total_releases", "notable_rate", "performance"])
            .merge(_rc, on="person_id", how="left")
            .fillna({"number_songs_collaborated": 0, "number_albums_collaborated": 0,
                     "total_releases": 0, "notable_releases": 0})
        )
        _ya = _persons_base["n_years_active"].where(_persons_base["n_years_active"] > 0)
        _tr = _persons_base["total_releases"].where(_persons_base["total_releases"] > 0)
        _persons_base["notable_rate"] = _persons_base["notable_releases"] / _tr
        _persons_base["performance"]  = _persons_base["notable_releases"] / _ya
        # groups: keep only Performer role; for other roles they appear with 0 releases
        _groups_base = df_group_career.copy()
        if _r != "Performer":
            _groups_base["number_songs_collaborated"]  = 0
            _groups_base["number_albums_collaborated"] = 0
            _groups_base["total_releases"]  = 0
            _groups_base["notable_releases"]= 0
            _groups_base["notable_rate"] = 0.0
            _groups_base["performance"]  = 0.0
        _base = pd.concat([_persons_base, _groups_base], ignore_index=True)

    # ── Filters ───────────────────────────────────────────────────────────────
    # skip the irrelevant min slider when a specific release type is selected
    _mask = _base["person_id"].notna()   # start with all-True mask
    if _t != "Album":
        _mask &= _base["number_songs_collaborated"]  >= min_songs.value
    if _t != "Song":
        _mask &= _base["number_albums_collaborated"] >= min_albums.value
    _mask &= (_base["n_years_active"] >= years_lo.value) & (_base["n_years_active"] <= years_hi.value)
    _mask &= (_base["last_release_year"].fillna(0) >= last_rel_lo.value) & \
             (_base["last_release_year"].fillna(9999) <= last_rel_hi.value)
    if genre_filter.value != "(All)":
        _mask &= _base["most_worked_genre"] == genre_filter.value
    if _r != "All" or _t != "All":
        _mask &= _base["total_releases"] > 0

    df_career_filtered = (
        _base[_mask]
        .sort_values("total_influenced", ascending=False)
        .reset_index(drop=True)
    )

    df_career_min_filtered = df_person_career[
        (df_person_career["number_songs_collaborated"] >= min_songs.value) &
        (df_person_career["number_albums_collaborated"] >= min_albums.value)
    ].reset_index(drop=True)
    return df_career_filtered, df_career_min_filtered


@app.cell
def _(mo):
    # Shared state: artist selection IDs, genre observer IDs, and notable-only toggle
    get_filter_ids, set_filter_ids = mo.state([])
    get_genre_obs_ids, set_genre_obs_ids = mo.state([])
    notable_toggle = mo.ui.switch(label="Notable only", value=False)
    return (
        get_filter_ids,
        get_genre_obs_ids,
        notable_toggle,
        set_filter_ids,
        set_genre_obs_ids,
    )


@app.cell
def _(df_career_filtered, get_filter_ids, mo, pd):
    # Artist selection table: shows filtered career data, pins previously selected artists
    _pinned = set(get_filter_ids())
    _display_cols = ["person_id", "entity_type", "person", "groups", "most_worked_genre",
                     "total_releases", "notable_releases", "total_influenced", "notable_rate",
                     "performance", "first_release_year", "last_release_year", "n_years_active"]
    _table_df = df_career_filtered[_display_cols].rename(columns={
        "person_id": "ID", "entity_type": "Type", "person": "Artist", "groups": "Groups",
        "most_worked_genre": "Top Genre",
        "total_releases": "Releases", "notable_releases": "Notable Releases",
        "total_influenced": "Influences", "notable_rate": "Notable Rate",
        "performance": "Notable/Year", "first_release_year": "Debut Year",
        "last_release_year": "Last Release", "n_years_active": "Years Active",
    })
    if _pinned:
        _in_sel = _table_df["ID"].isin(_pinned)
        _table_df = pd.concat(
            [_table_df[_in_sel], _table_df[~_in_sel]]
        ).reset_index(drop=True)
    _table_df.insert(0, "★", _table_df["ID"].isin(_pinned).map({True: "★", False: ""}))
    artist_table = mo.ui.table(_table_df, selection="multi",
                               label="Select artists to compare")
    return (artist_table,)


@app.cell
def _(
    artist_table,
    df_career_filtered,
    get_filter_ids,
    mo,
    set_filter_ids,
    set_genre_obs_ids,
):
    # Action buttons: pass current table selection to career analysis or genre observer
    pass_btn = mo.ui.button(
        label="Pass list to career analysis",
        on_click=lambda _: set_filter_ids(
            list(set(get_filter_ids()) | set(artist_table.value["ID"]))
            if len(artist_table.value) > 0 else get_filter_ids()
        ),
        kind="success",
    )
    genre_obs_btn = mo.ui.button(
        label="Pass list to Rising Star Selector",
        on_click=lambda _: set_genre_obs_ids(df_career_filtered["person_id"].tolist()),
        kind="neutral",
    )
    return genre_obs_btn, pass_btn


@app.cell
def _(alt, df_person_career, get_genre_obs_ids, mo, pd):
    # Genre Observer scatter: years active vs notable rate for the passed artist list
    _ids = set(get_genre_obs_ids())
    if not _ids:
        _scatter_df = pd.DataFrame()
    else:
        _scatter_df = df_person_career[df_person_career["person_id"].isin(_ids)].copy()

    if _scatter_df.empty:
        genre_obs_chart = mo.md(
            "*Click **Pass list to Rising Star Selector** to populate this chart.*"
        )
    else:
        def _primary_group(g):
            if not g or (isinstance(g, float)):
                return "(none)"
            parts = [p.strip() for p in str(g).split(",") if p.strip()]
            return parts[0] if parts else "(none)"

        _scatter_df["primary_group"] = _scatter_df["groups"].apply(_primary_group)
        _scatter_df["artist_label"] = _scatter_df.apply(
            lambda r: f"{r['person']} ({r['primary_group']})" if r["primary_group"] != "(none)" else r["person"],
            axis=1,
        )
        _scatter_df["dot_size"] = _scatter_df["total_releases"].clip(lower=1)
        _plot_df = _scatter_df.dropna(subset=["n_years_active", "notable_rate"]).copy()

        # Build co-located artists string for collision tooltips
        _co = (
            _plot_df.groupby(["n_years_active", "notable_rate"])["artist_label"]
            .apply(lambda s: " | ".join(s))
            .reset_index()
            .rename(columns={"artist_label": "co_located"})
        )
        _plot_df = _plot_df.merge(_co, on=["n_years_active", "notable_rate"], how="left")

        genre_obs_chart = mo.ui.altair_chart(
            alt.Chart(_plot_df)
            .mark_point(filled=True, opacity=0.65, stroke="white", strokeWidth=0.8)
            .encode(
                x=alt.X("n_years_active:Q", title="Years Active"),
                y=alt.Y("notable_rate:Q", title="Notable Rate"),
                color=alt.Color("artist_label:N", title="Artist (Group)",
                                legend=alt.Legend(orient="right")),
                shape=alt.Shape("primary_group:N", title="Group",
                                legend=alt.Legend(orient="right")),
                size=alt.Size("dot_size:Q", title="Total Releases",
                              scale=alt.Scale(range=[30, 500]),
                              legend=alt.Legend(values=[5, 10, 25, 50, 100])),
                tooltip=[
                    alt.Tooltip("co_located:N", title="Artists here"),
                    alt.Tooltip("person:N", title="Artist"),
                    alt.Tooltip("primary_group:N", title="Group"),
                    alt.Tooltip("n_years_active:Q", title="Years Active"),
                    alt.Tooltip("notable_rate:Q", title="Notable Rate", format=".3f"),
                    alt.Tooltip("total_releases:Q", title="Total Releases"),
                    alt.Tooltip("performance:Q", title="Notable/Year", format=".3f"),
                    alt.Tooltip("most_worked_genre:N", title="Top Genre"),
                ],
            )
            .properties(
                title="Years Active vs Notable Rate (size = Cum. Releases, color = Artist, shape = Group)",
                width=380, height=450,
            )
            .interactive()
        )
    return (genre_obs_chart,)


@app.cell
def _(
    df_group_career,
    df_person_career,
    get_filter_ids,
    mo,
    pd,
    set_filter_ids,
):
    # Career analysis controls: artist multi-select (pre-populated from pinned IDs) and clear button
    _pc = pd.concat([
        df_person_career[["person", "person_id"]],
        df_group_career[["person", "person_id"]],
    ]).drop_duplicates("person_id")
    # disambiguate names globally so duplicate names don't collapse in the dict
    _name_counts = _pc["person"].value_counts()
    _id_to_disp = {
        row["person_id"]: (
            row["person"] if _name_counts[row["person"]] == 1
            else f"{row['person']} [{row['person_id']}]"
        )
        for _, row in _pc.iterrows()
    }
    _options = {disp: pid for pid, disp in sorted(_id_to_disp.items(), key=lambda x: x[1])}
    _value = [_id_to_disp[i] for i in get_filter_ids() if i in _id_to_disp]
    artist_filter = mo.ui.multiselect(
        options=_options,
        value=_value,
        label="Compare artists",
    )
    clear_btn = mo.ui.button(
        label="Clear",
        on_click=lambda _: set_filter_ids([]),
        kind="warn",
    )
    return artist_filter, clear_btn


@app.cell
def _(artist_filter, df_group_edges, df_person_edges):
    # Step 1: Resolve selected artist IDs to display names and collect their songs/albums/groups
    # ── Step 1: Artist config — supports both Person and MusicalGroup IDs ─────
    _sel_ids    = set(artist_filter.value)
    _group_ids  = set(df_group_edges["id"])

    _sel_persons   = df_person_edges[df_person_edges["id"].isin(_sel_ids)]
    _sel_groups_df = df_group_edges[df_group_edges["id"].isin(_sel_ids)]

    # build unified id→display mapping (disambiguate when names clash)
    _all_rows = [{"id": r["id"], "name": r["name"]} for _, r in _sel_persons.iterrows()] + \
                [{"id": r["id"], "name": r["name"]} for _, r in _sel_groups_df.iterrows()]
    _all_name_series = [r["name"] for r in _all_rows]
    from collections import Counter as _Counter
    _name_counts_all = _Counter(_all_name_series)
    _id_to_display = {
        r["id"]: (r["name"] if _name_counts_all[r["name"]] == 1 else f"{r['name']} [{r['id']}]")
        for r in _all_rows
    }

    artist_display_to_real = {disp: r["name"] for r in _all_rows for disp in [_id_to_display[r["id"]]]}
    _INPUT_NAMES = set(_id_to_display.values())

    _song_role_cols = [
        "performer_of_songs", "composer_of_songs",
        "producer_of_songs", "lyricist_of_songs",
    ]
    _album_role_cols = [
        "performer_of_albums", "composer_of_albums",
        "producer_of_albums", "lyricist_of_albums",
    ]

    artist_groups      = {d: set() for d in _INPUT_NAMES}
    artist_song_names  = {d: set() for d in _INPUT_NAMES}
    artist_album_names = {d: set() for d in _INPUT_NAMES}

    # person works (all roles + group memberships)
    for _, _r in _sel_persons.iterrows():
        _d = _id_to_display[_r["id"]]
        if isinstance(_r.get("member_of"), list):
            artist_groups[_d].update(_r["member_of"])
        for _col in _song_role_cols:
            if isinstance(_r.get(_col), list):
                artist_song_names[_d].update(_r[_col])
        for _col in _album_role_cols:
            if isinstance(_r.get(_col), list):
                artist_album_names[_d].update(_r[_col])

    # group works (selected groups directly — performer only)
    for _, _r in _sel_groups_df.iterrows():
        _d = _id_to_display[_r["id"]]
        if isinstance(_r.get("performer_of_songs"), list):
            artist_song_names[_d].update(_r["performer_of_songs"])
        if isinstance(_r.get("performer_of_albums"), list):
            artist_album_names[_d].update(_r["performer_of_albums"])

    # add works performed by each group the PERSON artist belongs to
    for _, _gr in df_group_edges.iterrows():
        for _d in _INPUT_NAMES:
            if _gr["name"] in artist_groups[_d]:
                if isinstance(_gr.get("performer_of_songs"), list):
                    artist_song_names[_d].update(_gr["performer_of_songs"])
                if isinstance(_gr.get("performer_of_albums"), list):
                    artist_album_names[_d].update(_gr["performer_of_albums"])

    for _d in _INPUT_NAMES:
        print(
            f"{_d}  →  real: {artist_display_to_real[_d]}"
            f"  |  groups: {artist_groups[_d] or 'none'}"
            f"  |  songs: {len(artist_song_names[_d])}"
            f"  |  albums: {len(artist_album_names[_d])}"
        )
    return (
        artist_album_names,
        artist_display_to_real,
        artist_groups,
        artist_song_names,
    )


@app.cell
def _(
    artist_album_names,
    artist_display_to_real,
    artist_groups,
    artist_song_names,
    df_album_edges,
    df_group_edges,
    df_person_edges,
    df_song_edges,
    pd,
):
    # Step 2: Build per-artist release table with roles (composer/performer/etc.) for selected artists
    # ── Step 2: Release table — own works per artist ──────────────────────────
    _song_meta = df_song_edges.set_index("name")[
        ["genre", "release_date", "notable", "notoriety_date"]
    ].copy()
    _album_meta = df_album_edges.set_index("name")[
        ["genre", "release_date", "notable", "notoriety_date"]
    ].copy()

    def _get_meta(name, meta):
        if name not in meta.index:
            return {}
        m = meta.loc[name]
        return m.iloc[0] if isinstance(m, pd.DataFrame) else m

    def _parse_year(val):
        return pd.to_datetime(val, errors="coerce").year if val else None

    _rows = []
    for _artist in artist_display_to_real:
        for _name in artist_song_names[_artist]:
            _m = _get_meta(_name, _song_meta)
            _rows.append({
                "artist": _artist, "name": _name, "type": "song",
                "release_year": _parse_year(_m.get("release_date")),
                "notable": _m.get("notable"),
                "genre": _m.get("genre"),
                "notoriety_year": _parse_year(_m.get("notoriety_date")),
            })
        for _name in artist_album_names[_artist]:
            _m = _get_meta(_name, _album_meta)
            _rows.append({
                "artist": _artist, "name": _name, "type": "album",
                "release_year": _parse_year(_m.get("release_date")),
                "notable": _m.get("notable"),
                "genre": _m.get("genre"),
                "notoriety_year": _parse_year(_m.get("notoriety_date")),
            })

    _cols_works = ["artist", "name", "type", "release_year", "notable", "genre", "notoriety_year"]
    df_artist_works = (
        (pd.DataFrame(_rows)[_cols_works] if _rows else pd.DataFrame(columns=_cols_works))
        .drop_duplicates()
        .sort_values(["artist", "release_year"])
        .reset_index(drop=True)
    )

    # ── build work → roles lookup per artist ─────────────────────────────────
    _real_to_display = {v: k for k, v in artist_display_to_real.items()}
    _real_names = set(artist_display_to_real.values())

    _role_song_cols  = [("Performer", "performer_of_songs"),  ("Composer", "composer_of_songs"),
                        ("Producer",  "producer_of_songs"),   ("Lyricist", "lyricist_of_songs")]
    _role_album_cols = [("Performer", "performer_of_albums"), ("Composer", "composer_of_albums"),
                        ("Producer",  "producer_of_albums"),  ("Lyricist", "lyricist_of_albums")]

    # {display_name: {work_name: [roles]}}
    _song_roles  = {d: {} for d in artist_display_to_real}
    _album_roles = {d: {} for d in artist_display_to_real}

    for _, _pr in df_person_edges[df_person_edges["name"].isin(_real_names)].iterrows():
        _d = _real_to_display[_pr["name"]]
        for _role, _col in _role_song_cols:
            for _nm in (_pr.get(_col) if isinstance(_pr.get(_col), list) else []):
                _song_roles[_d].setdefault(_nm, []).append(_role)
        for _role, _col in _role_album_cols:
            for _nm in (_pr.get(_col) if isinstance(_pr.get(_col), list) else []):
                _album_roles[_d].setdefault(_nm, []).append(_role)

    # selected groups directly — their own songs/albums are Performer
    for _, _gr in df_group_edges[df_group_edges["name"].isin(_real_names)].iterrows():
        _d = _real_to_display[_gr["name"]]
        for _nm in (_gr.get("performer_of_songs") if isinstance(_gr.get("performer_of_songs"), list) else []):
            _roles = _song_roles[_d].setdefault(_nm, [])
            if "Performer" not in _roles:
                _roles.append("Performer")
        for _nm in (_gr.get("performer_of_albums") if isinstance(_gr.get("performer_of_albums"), list) else []):
            _roles = _album_roles[_d].setdefault(_nm, [])
            if "Performer" not in _roles:
                _roles.append("Performer")

    # group performer credits → Performer role on songs/albums (for person members)
    # pre-build reverse lookup: group_name → list of display_names that belong to it
    _group_to_display = {}
    for _d, _grps in artist_groups.items():
        for _grp in _grps:
            _group_to_display.setdefault(_grp, []).append(_d)
    _relevant_groups = set(_group_to_display.keys())
    for _, _gr in df_group_edges[df_group_edges["name"].isin(_relevant_groups)].iterrows():
        for _d in _group_to_display.get(_gr["name"], []):
            for _nm in (_gr.get("performer_of_songs") if isinstance(_gr.get("performer_of_songs"), list) else []):
                _roles = _song_roles[_d].setdefault(_nm, [])
                if "Performer" not in _roles:
                    _roles.append("Performer")
            for _nm in (_gr.get("performer_of_albums") if isinstance(_gr.get("performer_of_albums"), list) else []):
                _roles = _album_roles[_d].setdefault(_nm, [])
                if "Performer" not in _roles:
                    _roles.append("Performer")

    if df_artist_works.empty:
        df_artist_works["roles"] = pd.Series([], dtype=object)
    else:
        df_artist_works["roles"] = df_artist_works.apply(
            lambda r: sorted(
                _song_roles[r["artist"]].get(r["name"], [])
                if r["type"] == "song"
                else _album_roles[r["artist"]].get(r["name"], [])
            ),
            axis=1,
        )

    print(f"df_artist_works: {df_artist_works.shape}")
    # df_artist_works
    return (df_artist_works,)


@app.cell
def _(
    artist_album_names,
    artist_display_to_real,
    artist_groups,
    artist_song_names,
    df_album_edges,
    df_all_nodes,
    df_group_edges,
    df_person_edges,
    df_song_edges,
    pd,
    q3_df_influence_edges,
):
    # Step 3: Build influence tables — works that reference the artist (df_artist_influenced) and genres the artist drew from (df_artist_draws_from)
    # ── Step 3: Influence table — works that reference artist, group, or their songs/albums ──
    _song_meta2 = df_song_edges.set_index("name")[
        ["genre", "release_date", "notable", "notoriety_date"]
    ].copy()
    _album_meta2 = df_album_edges.set_index("name")[
        ["genre", "release_date", "notable", "notoriety_date"]
    ].copy()

    def _get_meta2(name, meta):
        if name not in meta.index:
            return {}
        m = meta.loc[name]
        return m.iloc[0] if isinstance(m, pd.DataFrame) else m

    def _parse_year2(val):
        return pd.to_datetime(val, errors="coerce").year if val else None

    # name → node ID lookup (and reverse: ID → what kind of target it is per artist)
    _name_to_id = {}
    for _nid, _nm in zip(df_all_nodes["id"], df_all_nodes["name"]):
        _name_to_id.setdefault(_nm, set()).add(_nid)

    # precompute each focus artist's earliest release year
    _artist_first_yr: dict = {}
    for _artist in artist_display_to_real:
        _min_yr = None
        for _nm in artist_song_names[_artist] | artist_album_names[_artist]:
            for _meta in (_song_meta2, _album_meta2):
                _yr = _parse_year2(_get_meta2(_nm, _meta).get("release_date"))
                if _yr is not None:
                    _min_yr = _yr if _min_yr is None else min(_min_yr, _yr)
        _artist_first_yr[_artist] = _min_yr

    # precompute debut year for every Person and MusicalGroup that appears as a
    # source in q3_df_influence_edges, so we can compute max(artist_debut, source_debut)
    _song_yr  = pd.to_datetime(df_song_edges["release_date"],  errors="coerce").dt.year
    _album_yr = pd.to_datetime(df_album_edges["release_date"], errors="coerce").dt.year
    _song_yr_map  = dict(zip(df_song_edges["name"],  _song_yr))
    _album_yr_map = dict(zip(df_album_edges["name"], _album_yr))

    _entity_debut: dict = {}
    _p_role_cols = ["performer_of_songs","composer_of_songs","producer_of_songs","lyricist_of_songs",
                    "performer_of_albums","composer_of_albums","producer_of_albums","lyricist_of_albums"]
    for _, _pr in df_person_edges.iterrows():
        _nm = _pr["name"]
        _yrs = []
        for _col in _p_role_cols:
            if isinstance(_pr.get(_col), list):
                for _w in _pr[_col]:
                    _y = _song_yr_map.get(_w) or _album_yr_map.get(_w)
                    if _y and not pd.isna(_y):
                        _yrs.append(int(_y))
        if _yrs:
            _entity_debut[_nm] = min(_yrs)

    for _, _gr in df_group_edges.iterrows():
        _nm = _gr["name"]
        _yrs = []
        for _col in ("performer_of_songs","performer_of_albums"):
            if isinstance(_gr.get(_col), list):
                for _w in _gr[_col]:
                    _y = _song_yr_map.get(_w) or _album_yr_map.get(_w)
                    if _y and not pd.isna(_y):
                        _yrs.append(int(_y))
        if _yrs:
            _entity_debut[_nm] = min(_yrs)

    _rows2 = []
    for _artist, _real in artist_display_to_real.items():
        # work IDs → tagged "work"
        _work_ids = set()
        for _nm in (artist_song_names[_artist] | artist_album_names[_artist]):
            _work_ids.update(_name_to_id.get(_nm, set()))

        # person IDs → tagged "person"
        _person_ids = set()
        for _nm in {_artist, _real}:
            _person_ids.update(_name_to_id.get(_nm, set()))

        # group IDs → tagged "group"
        _group_ids = set()
        for _nm in artist_groups[_artist]:
            _group_ids.update(_name_to_id.get(_nm, set()))

        _all_target_ids = _work_ids | _person_ids | _group_ids

        # build a lookup: target_id → referenced_as label
        _id_ref_as = {}
        for _id in _work_ids:
            _id_ref_as[_id] = "work"
        for _id in _person_ids:
            _id_ref_as[_id] = "person"
        for _id in _group_ids:
            _id_ref_as[_id] = "group"

        for _, _e in q3_df_influence_edges[
            q3_df_influence_edges["target"].isin(_all_target_ids) &
            ~q3_df_influence_edges["source"].isin(_all_target_ids)   # exclude self-influence
        ].iterrows():
            _src_name = _e["source_name"]
            _src_type = _e["source_type"]
            _ref_as = _id_ref_as.get(_e["target"], "work")

            if _src_type == "Song":
                _m = _get_meta2(_src_name, _song_meta2)
                _wtype = "song"
            elif _src_type == "Album":
                _m = _get_meta2(_src_name, _album_meta2)
                _wtype = "album"
            else:
                # Person or MusicalGroup as source — keep the row, no work metadata
                _m = {}
                _wtype = _src_type.lower()

            # year resolution cascade:
            # 1. source release_date (songs/albums)
            # 2. edge year field
            # 3. target work's release date (the cited song/album)
            # 4. artist's earliest release year (proxy for person-targeted edges)
            _ry = _parse_year2(_m.get("release_date"))
            if _ry is None:
                if pd.notna(_e.get("year")):
                    _ry = int(_e["year"])
                else:
                    _tnm, _ttp = _e.get("target_name"), _e.get("target_type")
                    if _ttp == "Song":
                        _ry = _parse_year2(_get_meta2(_tnm, _song_meta2).get("release_date"))
                    elif _ttp == "Album":
                        _ry = _parse_year2(_get_meta2(_tnm, _album_meta2).get("release_date"))
                    # Person/MusicalGroup target = someone cites the artist directly;
                    # the influence can't predate the artist's debut, so use
                    # max(artist_debut, source_entity_debut) as the proxy year
                    if _ry is None:
                        _a_debut = _artist_first_yr.get(_artist)
                        _s_debut = _entity_debut.get(_src_name)
                        if _a_debut is not None:
                            _ry = max(_a_debut, _s_debut) if _s_debut else _a_debut
            _rows2.append({
                "artist": _artist,
                "name": _src_name,
                "type": _wtype,
                "referenced_as": _ref_as,
                "edge_type": _e["edge_type"],
                "target_name": _e["target_name"],
                "target_type": _e["target_type"],
                "release_year": _ry,
                "genre": _m.get("genre"),
                "notoriety_year": _parse_year2(_m.get("notoriety_date")),
            })

    _cols_infl = ["artist", "name", "type", "referenced_as", "edge_type",
                  "target_name", "target_type", "release_year", "genre", "notoriety_year"]
    df_artist_influenced = (
        (pd.DataFrame(_rows2)[_cols_infl] if _rows2 else pd.DataFrame(columns=_cols_infl))
        .drop_duplicates()
        .sort_values(["artist", "referenced_as", "release_year"])
        .reset_index(drop=True)
    )


    # ── Step 3b: Genres that INFLUENCED the artist ────────────────────────────
    # Each selected artist's own works as SOURCE → target work genre = what inspired them
    _rows3 = []
    for _artist in artist_display_to_real:
        _own_work_ids = set()
        for _nm in (artist_song_names[_artist] | artist_album_names[_artist]):
            _own_work_ids.update(_name_to_id.get(_nm, set()))
        if not _own_work_ids:
            continue
        for _, _e in q3_df_influence_edges[
            q3_df_influence_edges["source"].isin(_own_work_ids) &
            ~q3_df_influence_edges["target"].isin(_own_work_ids)
        ].iterrows():
            _tgt_name = _e["target_name"]
            _tgt_type = _e["target_type"]
            if _tgt_type == "Song":
                _genre = _get_meta2(_tgt_name, _song_meta2).get("genre")
            elif _tgt_type == "Album":
                _genre = _get_meta2(_tgt_name, _album_meta2).get("genre")
            else:
                _genre = None
            if _genre:
                _rows3.append({
                    "artist": _artist,
                    "genre": _genre,
                    "edge_type": _e["edge_type"],
                    "source_name": _e["source_name"],
                    "target_name": _tgt_name,
                })
    df_artist_draws_from = (
        pd.DataFrame(_rows3)
        if _rows3
        else pd.DataFrame(columns=["artist", "genre", "edge_type", "source_name", "target_name"])
    )
    return df_artist_draws_from, df_artist_influenced


@app.cell
def _(
    alt,
    artist_display_to_real,
    df_album_edges,
    df_artist_draws_from,
    df_artist_influenced,
    df_artist_works,
    df_career_min_filtered,
    df_song_edges,
    mo,
    notable_toggle,
    pd,
):
    # Career analysis charts: cumulative releases, influence ratio, genre charts, bar charts for selected artists
    bin_size = 1
    chart_career = mo.md(
        "*Select artists in the table above, then click **Pass list** to view career analysis.*"
    )

    # ── all 3 focus artists, all types, all releases ──────────────────────────
    _works = df_artist_works.copy()
    if notable_toggle.value:
        _works = _works[_works["notable"] == True].copy()
    _infl = df_artist_influenced.copy()

    # enrich influenced with notable (person/group sources are never notable)
    _sn = df_song_edges.set_index("name")["notable"]
    _an = df_album_edges.set_index("name")["notable"]
    _infl["notable"] = _infl.apply(
        lambda r: bool(_sn.get(r["name"], False)) if r["type"] == "song"
                  else bool(_an.get(r["name"], False)) if r["type"] == "album"
                  else False,
        axis=1,
    )

    # ── build cumulative series ───────────────────────────────────────────────
    def _to_cumulative(_df):
        _df = _df.dropna(subset=["release_year"]).copy()
        _df["release_year"] = _df["release_year"].astype(int)
        _df["notable"] = _df["notable"].fillna(False).astype(bool)
        _df["_label"] = _df["name"] + " (" + _df["type"] + ")"
        if _df.empty:
            return pd.DataFrame(columns=["artist", "release_year", "count", "releases",
                                         "genres", "notable_count", "cumulative", "new_this_year"])

        _yr_min = _df["release_year"].min()
        _yr_max = _df["release_year"].max()
        _all_years = list(range(_yr_min, _yr_max + 1))

        _annual = (
            _df.groupby(["artist", "release_year"])
            .agg(
                count=("_label", "count"),
                releases=("_label", lambda x: " | ".join(sorted(x))),
                genres=("genre", lambda x: ", ".join(sorted(set(x.dropna())))),
                notable_count=("notable", "sum"),
            )
            .reset_index()
        )

        # fill every artist × year with 0 / empty so cumsum is continuous
        _artists = _annual["artist"].unique()
        _grid_df = pd.DataFrame(
            [(a, y) for a in _artists for y in _all_years],
            columns=["artist", "release_year"],
        )
        _annual = _grid_df.merge(_annual, on=["artist", "release_year"], how="left")
        _annual["count"] = _annual["count"].fillna(0).astype(int)
        _annual["notable_count"] = _annual["notable_count"].fillna(0).astype(int)
        _annual["releases"] = _annual["releases"].fillna("")
        _annual["genres"] = _annual["genres"].fillna("")
        _annual = _annual.sort_values(["artist", "release_year"])
        _annual["cumulative"] = _annual.groupby("artist")["count"].cumsum()
        _annual["new_this_year"] = _annual["count"]
        return _annual

    _parts = [
        _to_cumulative(_works).assign(series="Own Works"),
        _to_cumulative(_infl).assign(series="Influenced Works"),
    ]
    _combined = pd.concat(_parts, ignore_index=True)

    _yr_min = int(_combined["release_year"].min()) if not _combined.empty else 2000
    _yr_max = int(_combined["release_year"].max()) if not _combined.empty else 2025

    # ── top 5 genres per 2-year bin (matches the genre bar chart logic) ─────────
    _genre_src = (
        pd.concat(
            [
                df_song_edges[["genre", "release_date"]],
                df_album_edges[["genre", "release_date"]],
            ]
        )
        .dropna(subset=["genre"])
        .copy()
    )
    _genre_src["_yr"] = pd.to_datetime(
        _genre_src["release_date"], errors="coerce"
    ).dt.year
    _genre_src = _genre_src.dropna(subset=["_yr"])
    _genre_src["_bin"] = (_genre_src["_yr"] // 2) * 2
    _top5_by_bin = (
        _genre_src.groupby(["_bin", "genre"])
        .size()
        .reset_index(name="_cnt")
        .sort_values(["_bin", "_cnt"], ascending=[True, False])
        .groupby("_bin")
        .head(5)
        .groupby("_bin")["genre"]
        .apply(set)
        .to_dict()
    )

    def _check_top5(r):
        if r["series"] != "Own Works" or r["new_this_year"] <= 0:
            return False
        _bin = (int(r["release_year"]) // 2) * 2
        _top = _top5_by_bin.get(_bin, set())
        return any(g.strip() in _top for g in str(r["genres"]).split(",") if g.strip())

    _combined["has_top5"] = (
        _combined.apply(_check_top5, axis=1) if not _combined.empty else False
    )

    # ── debut map: first year with an actual release per artist ──────────────
    _debut_map = (
        _combined[
            (_combined["series"] == "Own Works") & (_combined["new_this_year"] > 0)
        ]
        .groupby("artist")["release_year"].min()
        .to_dict()
    )
    # Chart 1 always uses calendar year
    _combined["x_year"] = _combined["release_year"]
    _x_title = "Release Year"
    _x_min = int(_combined["x_year"].min()) if not _combined.empty else 1980
    _x_max = int(_combined["x_year"].max()) if not _combined.empty else 2025

    # ── crossover year: derive directly from _combined (no re-read needed) ──────
    _cross_rows = []
    for _artist in _combined["artist"].unique():
        _oc = (
            _combined[(_combined["artist"] == _artist) & (_combined["series"] == "Own Works")]
            [["release_year", "cumulative"]].rename(columns={"cumulative": "cum_own"})
        )
        _ic = (
            _combined[(_combined["artist"] == _artist) & (_combined["series"] == "Influenced Works")]
            [["release_year", "cumulative"]].rename(columns={"cumulative": "cum_inf"})
        )
        if _oc.empty or _ic.empty:
            continue
        _g = (
            _oc.merge(_ic, on="release_year", how="outer")
            .sort_values("release_year")
            .ffill()
            .fillna(0)
        )
        _g["_prev_behind"] = _g["cum_inf"].shift(1, fill_value=0) < _g["cum_own"].shift(1, fill_value=1)
        _crossings = _g[(_g["cum_inf"] >= _g["cum_own"]) & _g["_prev_behind"]]
        if not _crossings.empty:
            _cross_rows.append({"artist": _artist, "crossover_year": int(_crossings.iloc[-1]["release_year"])})
    _crossover = pd.DataFrame(_cross_rows)

    # ── build cumulative series tables ────────────────────────────────────────
    _own_cum = _combined[_combined["series"] == "Own Works"][
        ["artist", "release_year", "cumulative"]
    ].rename(columns={"cumulative": "cum_own"})
    _inf_cum = _combined[_combined["series"] == "Influenced Works"][
        ["artist", "release_year", "cumulative"]
    ].rename(columns={"cumulative": "cum_inf"})
    # derive from _combined — no need to re-read source tables
    _first_yr = (
        _combined[_combined["series"] == "Own Works"]
        .groupby("artist")["release_year"].min()
        .rename("first_release_year").reset_index()
    )
    _first_inf_yr = (
        _combined[_combined["series"] == "Influenced Works"]
        .groupby("artist")["release_year"].min()
        .rename("first_inf_year").reset_index()
    )
    _bs = bin_size
    _raw_idx = (
        _own_cum.merge(_inf_cum, on=["artist", "release_year"], how="left")
        .merge(_first_yr, on="artist")
        .merge(_first_inf_yr, on="artist")
    )
    _raw_idx = _raw_idx.sort_values(["artist", "release_year"])
    # ffill so cumulative doesn't drop after last influence data point;
    # fill any remaining NaN (pre-first-influence years) with 0
    _raw_idx["cum_inf"] = _raw_idx.groupby("artist")["cum_inf"].transform(
        lambda s: s.ffill().fillna(0)
    )
    if _bs == 1:
        df_effect_idx = _raw_idx.copy()
        df_effect_idx["bin_year"] = df_effect_idx["release_year"]
    else:
        # assign each year to its bin (start of bin)
        _raw_idx["bin_year"] = (_raw_idx["release_year"] // _bs) * _bs
        # take the last cumulative value in each bin (= value at end of bin)
        df_effect_idx = (
            _raw_idx.sort_values("release_year")
            .groupby(["artist", "bin_year", "first_release_year", "first_inf_year"])
            .agg(cum_own=("cum_own", "last"), cum_inf=("cum_inf", "last"))
            .reset_index()
        )
        df_effect_idx["release_year"] = df_effect_idx["bin_year"]

    # Chart 2 always uses cohort year (years since debut), clipped to 0
    df_effect_idx["x_year"] = df_effect_idx.apply(
        lambda r: max(0, r["release_year"] - _debut_map.get(r["artist"], r["release_year"])),
        axis=1,
    )

    # crossover year for Chart 1 (calendar year)
    if not _crossover.empty:
        _crossover = _crossover.copy()
        _crossover["cx_year"] = _crossover["crossover_year"]
    df_crossover = _crossover

    _sel = alt.selection_point(fields=["artist"], bind="legend")
    _sel_series = alt.selection_point(fields=["series"], bind="legend")

    _x_shared = alt.X(
        "x_year:Q",
        scale=alt.Scale(domain=[_x_min, _x_max], nice=False),
        title=_x_title,
        axis=alt.Axis(format="d", tickMinStep=1),
    )

    _lines = (
        alt.Chart(_combined)
        .mark_line(strokeWidth=2.5)
        .encode(
            x=_x_shared,
            y=alt.Y("cumulative:Q", title="Cumulative Works",
                    axis=alt.Axis(orient="left", labels=True, ticks=True)),
            color=alt.Color("artist:N", legend=alt.Legend(title="Artist", orient="none", legendX=425, legendY=5)),
            strokeDash=alt.StrokeDash(
                "series:N",
                scale=alt.Scale(
                    domain=["Own Works", "Influenced Works"], range=[[1, 0], [6, 4]]
                ),
                legend=alt.Legend(title="Series", orient="none", legendX=425, legendY=90),
            ),
            opacity=alt.condition(_sel & _sel_series, alt.value(1.0), alt.value(0.08)),
            tooltip=[
                alt.Tooltip("artist:N"),
                alt.Tooltip("series:N", title="Series"),
                alt.Tooltip("x_year:Q", title=_x_title, format="d"),
                alt.Tooltip("release_year:Q", title="Calendar year", format="d"),
                alt.Tooltip("cumulative:Q", title="Cumulative"),
                alt.Tooltip("new_this_year:Q", title="New this year"),
                alt.Tooltip("notable_count:Q", title="Notable"),
                alt.Tooltip("genres:N", title="Genre(s)"),
                alt.Tooltip("releases:N", title="Released"),
            ],
        )
    )

    _points = (
        alt.Chart(_combined[_combined["new_this_year"] > 0])
        .mark_point(size=55, filled=True)
        .encode(
            x=alt.X("x_year:Q"),
            y=alt.Y("cumulative:Q"),
            color=alt.Color("artist:N", legend=None),
            opacity=alt.condition(_sel & _sel_series, alt.value(0.9), alt.value(0.08)),
            tooltip=[
                alt.Tooltip("artist:N"),
                alt.Tooltip("series:N", title="Series"),
                alt.Tooltip("x_year:Q", title=_x_title, format="d"),
                alt.Tooltip("release_year:Q", title="Calendar year", format="d"),
                alt.Tooltip("cumulative:Q", title="Cumulative"),
                alt.Tooltip("new_this_year:Q", title="New this year"),
                alt.Tooltip("notable_count:Q", title="Notable"),
                alt.Tooltip("genres:N", title="Genre(s)"),
                alt.Tooltip("releases:N", title="Released"),
            ],
        )
    )

    # ── crossover fade: soft vertical band per artist ────────────────────────
    _cross_layers = []
    if not df_crossover.empty:
        _cx = df_crossover
        if not _cx.empty:
            _cross_layers.append(
                alt.Chart(_cx)
                .mark_rule(strokeWidth=18, opacity=0.12)
                .encode(
                    x=alt.X("cx_year:Q"),
                    color=alt.Color("artist:N", legend=None),
                    opacity=alt.condition(_sel, alt.value(0.18), alt.value(0.04)),
                )
            )
            _cross_layers.append(
                alt.Chart(_cx)
                .mark_rule(strokeWidth=2, opacity=0.7, strokeDash=[5, 3])
                .encode(
                    x=alt.X("cx_year:Q"),
                    color=alt.Color("artist:N", legend=None),
                    opacity=alt.condition(_sel, alt.value(0.8), alt.value(0.1)),
                    tooltip=[
                        alt.Tooltip("artist:N"),
                        alt.Tooltip("cx_year:Q", title="Influence > Releases from", format="d"),
                        alt.Tooltip("crossover_year:Q", title="Calendar year", format="d"),
                    ],
                )
            )

    # ── top-5 genre rings: hollow circle around qualifying own-work points ─────
    _top3_rings = (
        alt.Chart(
            _combined[_combined["has_top5"]] if not _combined.empty else _combined
        )
        .mark_point(size=160, filled=False, strokeWidth=2)
        .encode(
            x=alt.X("x_year:Q"),
            y=alt.Y("cumulative:Q"),
            color=alt.Color("artist:N", legend=None),
            opacity=alt.condition(_sel & _sel_series, alt.value(0.9), alt.value(0.0)),
            tooltip=[
                alt.Tooltip("artist:N"),
                alt.Tooltip("x_year:Q", title=_x_title, format="d"),
                alt.Tooltip("release_year:Q", title="Calendar year", format="d"),
                alt.Tooltip("cumulative:Q", title="Cumulative"),
                alt.Tooltip("new_this_year:Q", title="New this year"),
                alt.Tooltip("notable_count:Q", title="Notable"),
                alt.Tooltip("genres:N", title="Genre(s)"),
                alt.Tooltip("releases:N", title="Released"),
            ],
        )
    )

    _release_layers = [_lines, _points, _top3_rings]

    _chart_releases = (
        alt.layer(*_release_layers)
        .add_params(_sel, _sel_series)
        .properties(
            title=alt.TitleParams(
                "Cumulative Works — Solid: Own Releases  |  Dashed: Works Influenced by Artist  |  ○ Top-5 Genre",
                fontSize=13,
            ),
            width=420,
            height=270,
        )
    )

    # ── derive annual metrics from df_effect_idx ─────────────────────────────
    _m = df_effect_idx.sort_values(["artist", "x_year"]).copy()
    # avg release rate = cum_own / years since first release (min 1 to avoid /0)
    _m["release_cohort_yrs"] = (_m["release_year"] - _m["first_release_year"]).clip(
        lower=1
    )
    _m["avg_release_rate"] = _m["cum_own"] / _m["release_cohort_yrs"]
    # avg influence rate = cum_inf / years since first influence (min 1 to avoid /0)
    _m["inf_cohort_yrs"] = (_m["release_year"] - _m["first_inf_year"]).clip(lower=1)
    _m["avg_inf_rate"] = _m["cum_inf"] / _m["inf_cohort_yrs"]
    # ratio only defined once the artist has at least one influenced work
    # treat NaN cum_inf as 0 (years before first influenced work)
    _m["cum_inf"] = _m["cum_inf"].fillna(0)
    _m["avg_inf_rate"] = _m["cum_inf"] / _m["inf_cohort_yrs"]

    # Original: release cohort yrs for own, influence cohort yrs for influenced
    _m["release_vs_inf"] = _m["avg_inf_rate"] / _m["avg_release_rate"].clip(lower=1e-9)

    # Version 3: both divided by years since first INFLUENCE — cohort yrs cancel → cum_inf / cum_own
    _m["ratio_inf_anchor"] = _m["cum_inf"] / _m["cum_own"].clip(lower=1e-9)

    _x_enc = alt.X(
        "x_year:Q",
        scale=alt.Scale(domain=[0, 60], nice=False),
        title="Years since debut",
        axis=alt.Axis(format="d", tickMinStep=1),
    )

    _y_scale = alt.Scale(zero=True)
    _y_fmt = alt.Axis(format=".2f")

    # ── Chart 2: shaded area with pre/post breakout colour split ─────────────
    _line = (
        alt.Chart(_m)
        .mark_line(strokeWidth=2.5)
        .encode(
            x=_x_enc,
            y=alt.Y(
                "ratio_inf_anchor:Q",
                title="Cum Influenced / Cum Releases",
                scale=_y_scale,
                axis=_y_fmt,
            ),
            color=alt.Color("artist:N", legend=alt.Legend(title="Artist", orient="right")),
            opacity=alt.condition(_sel, alt.value(0.95), alt.value(0.04)),
            tooltip=[
                alt.Tooltip("artist:N"),
                alt.Tooltip("x_year:Q", title="Years since debut", format="d"),
                alt.Tooltip("ratio_inf_anchor:Q", title="Ratio", format=".3f"),
                alt.Tooltip("cum_inf:Q", title="Cum. influenced"),
                alt.Tooltip("cum_own:Q", title="Cum. own releases"),
            ],
        )
    )
    _breakeven = (
        alt.Chart(pd.DataFrame({"y": [1]}))
        .mark_rule(color="#aaa", strokeWidth=1.5, strokeDash=[5, 3])
        .encode(y=alt.Y("y:Q"))
    )
    _chart_ratio_inf = alt.layer(_line, _breakeven).properties(
        title=alt.TitleParams(
            "Influence Ratio — Cum Influenced / Cum Releases  (cohort: years since debut)",
            fontSize=12,
        ),
        width=420,
        height=165,
    )

    # ── Chart H: Genres Influenced per Artist (normalized horizontal bar) ────────
    _inf_genre_counts = (
        df_artist_draws_from[df_artist_draws_from["artist"].isin(set(artist_display_to_real.keys()))]
        .dropna(subset=["genre"])
        .groupby(["artist", "genre"])
        .size()
        .reset_index(name="count")
    )
    _inf_genre_totals = _inf_genre_counts.groupby("artist")["count"].transform("sum")
    _inf_genre_counts["share"] = _inf_genre_counts["count"] / _inf_genre_totals
    _chart_inf_genre = (
        alt.Chart(_inf_genre_counts)
        .mark_bar()
        .encode(
            x=alt.X("share:Q", title="Share of Influences", axis=alt.Axis(format="%"), stack="zero"),
            y=alt.Y("artist:N", title="Artist"),
            color=alt.Color("genre:N", title="Genre", legend=alt.Legend(orient="right")),
            order=alt.Order("count:Q", sort="descending"),
            tooltip=[
                alt.Tooltip("artist:N", title="Artist"),
                alt.Tooltip("genre:N", title="Genre"),
                alt.Tooltip("count:Q", title="Influences"),
                alt.Tooltip("share:Q", title="Share", format=".1%"),
            ],
        )
        .properties(
            title="Genres Influenced per Artist (normalized)",
            width=220,
            height=110,
        )
    )

    # ── Chart C: Influence Type Breakdown (stacked bar) ──────────────────────
    _real_to_display = {v: k for k, v in artist_display_to_real.items()}
    _real_sel = set(artist_display_to_real.values())
    _edge_label = {
        "InStyleOf":          "In Style Of",
        "InterpolatesFrom":   "Interpolates",
        "LyricalReferenceTo": "Lyrical Ref",
        "DirectlySamples":    "Samples",
        "CoverOf":            "Cover",
    }
    _inf_type_df = (
        df_artist_influenced[df_artist_influenced["artist"].isin(set(artist_display_to_real.keys()))]
        .copy()
        .assign(influence_type=lambda d: d["edge_type"].map(_edge_label).fillna(d["edge_type"]))
        .groupby(["artist", "influence_type"])
        .size()
        .reset_index(name="count")
    )
    _chart_source_breakdown = (
        alt.Chart(_inf_type_df)
        .mark_bar()
        .encode(
            x=alt.X("artist:N", title="Artist", axis=alt.Axis(labelAngle=-20)),
            y=alt.Y("count:Q", title="Count", stack="zero"),
            color=alt.Color("influence_type:N", title="Influence Type"),
            order=alt.Order("count:Q", sort="descending"),
            tooltip=[
                alt.Tooltip("artist:N", title="Artist"),
                alt.Tooltip("influence_type:N", title="Type"),
                alt.Tooltip("count:Q", title="Count"),
            ],
        )
        .properties(
            title="Influence Type Breakdown",
            width=220,
            height=145,
        )
    )

    # ── Chart D: Sub-metric Profile (min-max normalized within the filtered cohort) ──
    _norm_map = {
        "influence_efficiency":  "Spread",
        "notable_rate":          "Notable Rate",
        "breakout_speed_raw":    "Breakout Speed",
        "performance":           "Performance",
    }

    # compute breakout_speed on filtered cohort, then min-max within that cohort
    _metrics_df = df_career_min_filtered.copy()
    _bd = _metrics_df["breakout_delay"].copy()
    _bd_inv = 1.0 / _bd.where(_bd > 0)   # NaN for 0 or negative delay
    _bd_inv[_bd.isna() | (_bd <= 0)] = 0.0
    _metrics_df["breakout_speed_raw"] = _bd_inv

    def _minmax_global(s):
        s = s.fillna(0)
        mn, mx = s.min(), s.max()
        return (s - mn) / (mx - mn) if mx > mn else s * 0.0

    for _col in _norm_map:
        _metrics_df[_col + "_norm"] = _minmax_global(_metrics_df[_col])

    _profile_sel = _metrics_df[_metrics_df["person"].isin(_real_sel)].copy()

    _profile_sel["person"] = _profile_sel["person"].map(
        lambda n: _real_to_display.get(n, n)
    )
    _profile_long = (
        _profile_sel[["person"] + [c + "_norm" for c in _norm_map]]
        .melt(id_vars="person", var_name="metric", value_name="normalized_value")
    )
    _profile_long["metric"] = _profile_long["metric"].map(
        {c + "_norm": v for c, v in _norm_map.items()}
    )

    _chart_profile = (
        alt.Chart(_profile_long)
        .mark_bar(clip=True)
        .encode(
            x=alt.X(
                "normalized_value:Q",
                title="Normalized Value (0=lowest, 1=highest in dataset)",
                scale=alt.Scale(domain=[0, 1]),
            ),
            y=alt.Y("metric:N", title="Metric"),
            color=alt.Color("person:N", title="Artist"),
            yOffset=alt.YOffset("person:N"),
            tooltip=[
                alt.Tooltip("person:N", title="Artist"),
                alt.Tooltip("metric:N", title="Metric"),
                alt.Tooltip("normalized_value:Q", title="Normalized", format=".3f"),
            ],
        )
        .properties(
            title="Sub-metric Profile (min-max vs all artists)",
            width=220,
            height=145,
        )
    )

    # ── Chart E: Role Distribution ─────────────────────────────────────────────
    # Use df_artist_works (which already has full roles per work including group credits)
    # Explode roles so each role instance is a separate row, then count per artist×role
    _works_sel = df_artist_works[df_artist_works["artist"].isin(
        set(artist_display_to_real.keys())
    )].copy()
    _works_exploded = _works_sel[_works_sel["roles"].map(len) > 0].explode("roles")
    _role_df = (
        _works_exploded.groupby(["artist", "roles"])
        .size()
        .reset_index(name="count")
        .rename(columns={"roles": "role"})
    )

    _chart_roles = (
        alt.Chart(_role_df)
        .mark_bar()
        .encode(
            x=alt.X("artist:N", title="Artist"),
            y=alt.Y("count:Q", title="Count", stack="zero"),
            color=alt.Color("role:N", title="Role"),
            tooltip=[
                alt.Tooltip("artist:N", title="Artist"),
                alt.Tooltip("role:N", title="Role"),
                alt.Tooltip("count:Q", title="Count"),
            ],
        )
        .properties(
            title="Repertoire Role Distribution",
            width=220,
            height=145,
        )
    )

    # ── Chart F: Work Distribution (songs vs albums) ──────────────────────────
    _work_dist = (
        df_artist_works[df_artist_works["artist"].isin(set(artist_display_to_real.keys()))]
        .groupby(["artist", "type"])
        .size()
        .reset_index(name="count")
    )
    _chart_work_dist = (
        alt.Chart(_work_dist)
        .mark_bar()
        .encode(
            x=alt.X("artist:N", title="Artist"),
            y=alt.Y("count:Q", title="Count", stack="zero"),
            color=alt.Color("type:N", title="Type",
                            scale=alt.Scale(domain=["song", "album"],
                                            range=["#4C78A8", "#F58518"])),
            tooltip=[
                alt.Tooltip("artist:N", title="Artist"),
                alt.Tooltip("type:N", title="Type"),
                alt.Tooltip("count:Q", title="Count"),
            ],
        )
        .properties(
            title="Work Distribution (Songs vs Albums)",
            width=220,
            height=145,
        )
    )

    # ── Chart G: Genre Distribution (normalized stacked bar) ──────────────────
    _genre_counts = (
        df_artist_works[df_artist_works["artist"].isin(set(artist_display_to_real.keys()))]
        .dropna(subset=["genre"])
        .groupby(["artist", "genre"])
        .size()
        .reset_index(name="count")
    )
    # compute share per artist so bars are normalized to 100%
    _genre_totals = _genre_counts.groupby("artist")["count"].transform("sum")
    _genre_counts["share"] = _genre_counts["count"] / _genre_totals

    _chart_genre_dist = (
        alt.Chart(_genre_counts)
        .mark_bar()
        .encode(
            x=alt.X("share:Q", title="Share of Works", axis=alt.Axis(format="%"), stack="zero"),
            y=alt.Y("artist:N", title="Artist"),
            color=alt.Color("genre:N", title="Genre", legend=alt.Legend(orient="right")),
            order=alt.Order("count:Q", sort="descending"),
            tooltip=[
                alt.Tooltip("artist:N", title="Artist"),
                alt.Tooltip("genre:N", title="Genre"),
                alt.Tooltip("count:Q", title="Works"),
                alt.Tooltip("share:Q", title="Share", format=".1%"),
            ],
        )
        .properties(
            title="Genre Distribution per Artist (normalized)",
            width=220,
            height=110,
        )
    )

    chart_career = (
        alt.hconcat(
            # Left: line charts (shared artist color)
            alt.vconcat(_chart_releases, _chart_ratio_inf)
                .resolve_scale(color="shared")
                .resolve_axis(y="independent"),
            # Right: 2×2 bar charts + both genre charts side-by-side below
            alt.vconcat(
                alt.hconcat(_chart_source_breakdown, _chart_work_dist).resolve_scale(color="independent"),
                alt.hconcat(_chart_roles, _chart_profile).resolve_scale(color="independent"),
                alt.hconcat(_chart_genre_dist, _chart_inf_genre).resolve_scale(color="independent"),
            ).resolve_scale(color="independent"),
        ).resolve_scale(color="independent")
    )
    if not artist_display_to_real:
        chart_career = mo.md(
            "*Select artists in the table above, then click **Pass list** to view career analysis.*"
        )
    return (chart_career,)


@app.cell
def _(
    artist_filter,
    artist_table,
    chart_career,
    clear_btn,
    df_career_filtered,
    dist_charts_view,
    genre_filter,
    genre_obs_btn,
    genre_obs_chart,
    last_rel_hi,
    last_rel_lo,
    min_albums,
    min_songs,
    mo,
    notable_toggle,
    pass_btn,
    release_type,
    role_filter,
    years_hi,
    years_lo,
):
    # Q3 dashboard: assemble all controls, table, career charts, and genre observer into the final layout
    _n_total    = len(df_career_filtered)
    _n_selected = len(artist_filter.value)

    _header = mo.md(
        f"## Q3 — Artist Career Explorer\n"
        f"Cohort: **{_n_total}** artists "
        + (f"| **{_n_selected}** in career analysis" if _n_selected > 0 else "| pass artists to career analysis")
    )

    _controls = mo.hstack(
        [min_songs, min_albums, genre_filter, role_filter, release_type, years_lo, years_hi, last_rel_lo, last_rel_hi],
        justify="start",
        gap="1rem",
    )

    _left_panel = mo.vstack([
        mo.md("#### Population Context"),
        dist_charts_view,
    ], gap="0.25rem")

    _right_panel = mo.vstack([
        mo.md("#### Filter & Select Artists  *(multi-select rows)*"),
        artist_table,
        mo.hstack([pass_btn, genre_obs_btn], gap="1rem"),
    ], gap="0.25rem")

    _top_row = mo.hstack([_left_panel, _right_panel], gap="0.5rem", align="start", widths=[None, 1])

    _career_section = mo.vstack([
        mo.hstack([mo.md("### Career Analysis"), notable_toggle, clear_btn], align="center", gap="1rem"),
        artist_filter,
        chart_career,
    ])

    _sep = mo.md('<div style="border-left:2px solid #d0d0d0;align-self:stretch;margin:0 0.5rem"></div>')

    _genre_obs_section = mo.vstack([
        mo.md("### Rising Star Selector"),
        genre_obs_chart,
    ])

    _analysis_row = mo.hstack([_career_section, _sep, _genre_obs_section], gap="1.5rem", align="start")

    mo.vstack([_header, _controls, _top_row, _analysis_row], gap="1.5rem")
    return


if __name__ == "__main__":
    app.run()
