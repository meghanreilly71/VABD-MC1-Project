import marimo

__generated_with = "0.19.2"
app = marimo.App(width="medium")


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
    return defaultdict, json, mo, mpatches, nx, pd, plt


@app.cell
def _(defaultdict, mpatches, nx, plt):
    # Visualise the graph schema: node types and edge types
    schema = nx.MultiDiGraph()

    node_types = ['Person', 'MusicalGroup', 'RecordLabel', 'Song', 'Album']
    node_colors = {
        'Person': '#4ECDC4',
        'MusicalGroup': '#FF6B6B',
        'RecordLabel': '#FFE66D',
        'Song': '#95E1D3',
        'Album': '#F38181'
    }
    for nt in node_types:
        schema.add_node(nt)

    schema_edges = [
        ('Person', 'Song', 'PerformerOf'),
        ('Person', 'Album', 'PerformerOf'),
        ('MusicalGroup', 'Song', 'PerformerOf'),
        ('MusicalGroup', 'Album', 'PerformerOf'),
        ('Person', 'Song', 'ComposerOf'),
        ('Person', 'Album', 'ComposerOf'),
        ('Person', 'Song', 'ProducerOf'),
        ('Person', 'Album', 'ProducerOf'),
        ('Person', 'Person', 'ProducerOf'),
        ('Person', 'MusicalGroup', 'ProducerOf'),
        ('RecordLabel', 'Song', 'ProducerOf'),
        ('RecordLabel', 'Album', 'ProducerOf'),
        ('Person', 'Song', 'LyricistOf'),
        ('Person', 'Album', 'LyricistOf'),
        ('Song', 'RecordLabel', 'RecordedBy'),
        ('Album', 'RecordLabel', 'RecordedBy'),
        ('Song', 'RecordLabel', 'DistributedBy'),
        ('Album', 'RecordLabel', 'DistributedBy'),
        ('Song', 'Song', 'InStyleOf'),
        ('Song', 'Album', 'InStyleOf'),
        ('Song', 'Person', 'InStyleOf'),
        ('Song', 'MusicalGroup', 'InStyleOf'),
        ('Album', 'Song', 'InStyleOf'),
        ('Album', 'Album', 'InStyleOf'),
        ('Album', 'Person', 'InStyleOf'),
        ('Album', 'MusicalGroup', 'InStyleOf'),
        ('Song', 'Song', 'InterpolatesFrom'),
        ('Song', 'Album', 'InterpolatesFrom'),
        ('Album', 'Song', 'InterpolatesFrom'),
        ('Album', 'Album', 'InterpolatesFrom'),
        ('Song', 'Song', 'CoverOf'),
        ('Song', 'Album', 'CoverOf'),
        ('Album', 'Song', 'CoverOf'),
        ('Album', 'Album', 'CoverOf'),
        ('Song', 'Song', 'LyricalReferenceTo'),
        ('Song', 'Album', 'LyricalReferenceTo'),
        ('Album', 'Song', 'LyricalReferenceTo'),
        ('Album', 'Album', 'LyricalReferenceTo'),
        ('Song', 'Song', 'DirectlySamples'),
        ('Song', 'Album', 'DirectlySamples'),
        ('Album', 'Song', 'DirectlySamples'),
        ('Album', 'Album', 'DirectlySamples'),
        ('Person', 'MusicalGroup', 'MemberOf'),
    ]

    for src, tgt, etype in schema_edges:
        schema.add_edge(src, tgt, label=etype)

    fig, ax = plt.subplots(figsize=(14, 10))
    pos = {
        'Person': (-1, 1),
        'MusicalGroup': (1, 1),
        'RecordLabel': (0, -1),
        'Song': (-1.5, 0),
        'Album': (1.5, 0),
    }

    for nt in node_types:
        nx.draw_networkx_nodes(schema, pos, nodelist=[nt], node_color=node_colors[nt],
                               node_size=3000, ax=ax)
    nx.draw_networkx_labels(schema, pos, font_size=10, font_weight='bold', ax=ax)

    edge_colors_map = {
        'PerformerOf': '#2196F3', 'ComposerOf': '#4CAF50', 'ProducerOf': '#FF9800',
        'LyricistOf': '#9C27B0', 'RecordedBy': '#795548', 'DistributedBy': '#607D8B',
        'InStyleOf': '#E91E63', 'InterpolatesFrom': '#00BCD4', 'CoverOf': '#F44336',
        'LyricalReferenceTo': '#CDDC39', 'DirectlySamples': '#FF5722', 'MemberOf': '#3F51B5'
    }

    edge_groups = defaultdict(list)
    for src, tgt, etype in schema_edges:
        edge_groups[(src, tgt)].append(etype)

    for (src, tgt), etypes in edge_groups.items():
        for i, etype in enumerate(etypes):
            rad = 0.1 + i * 0.15
            nx.draw_networkx_edges(schema, pos, edgelist=[(src, tgt)], ax=ax,
                                   edge_color=edge_colors_map[etype], width=1.5,
                                   connectionstyle=f'arc3,rad={rad}',
                                   arrows=True, arrowsize=15, alpha=0.7)

    legend_handles = [mpatches.Patch(color=c, label=e) for e, c in edge_colors_map.items()]
    ax.legend(handles=legend_handles, loc='lower left', fontsize=8, ncol=2, title='Edge Types')
    ax.set_title('MC1 Graph Schema: Node Types & Edge Types', fontsize=14, fontweight='bold')
    ax.axis('off')
    plt.tight_layout()
    fig
    return


@app.cell
def _(json, pd):
    with open('MC1_graph.json', 'r') as f:
        data = json.load(f)

    df_all_nodes = pd.DataFrame(data['nodes'])
    df_all_edges = pd.DataFrame(data['links'])

    # Lookup dicts
    id_to_name = dict(zip(df_all_nodes['id'], df_all_nodes['name']))
    id_to_type = dict(zip(df_all_nodes['id'], df_all_nodes['Node Type']))

    # Resolve names on edges once
    df_all_edges['source_name'] = df_all_edges['source'].map(id_to_name)
    df_all_edges['target_name'] = df_all_edges['target'].map(id_to_name)

    print(f"Nodes: {len(df_all_nodes)}  |  Edges: {len(df_all_edges)}")
    print(f"\nNode types:\n{df_all_nodes['Node Type'].value_counts().to_string()}")
    print(f"\nEdge types:\n{df_all_edges['Edge Type'].value_counts().to_string()}")
    return df_all_edges, df_all_nodes, id_to_type


@app.cell
def _(mo):
    mo.md(r"""
    ## Base Node Tables
    """)
    return


@app.cell
def _(df_all_nodes):
    # Songs
    song_cols = ['id', 'name', 'genre', 'release_date', 'single', 'notable', 'notoriety_date', 'written_date']
    song_cols = [c for c in song_cols if c in df_all_nodes.columns]
    df_songs = df_all_nodes[df_all_nodes['Node Type'] == 'Song'][song_cols].copy().reset_index(drop=True)
    print(f"df_songs: {df_songs.shape}")
    df_songs.head()
    return (df_songs,)


@app.cell
def _(df_all_nodes):
    # Albums
    album_cols = ['id', 'name', 'genre', 'release_date', 'notable', 'notoriety_date', 'written_date']
    album_cols = [c for c in album_cols if c in df_all_nodes.columns]
    df_albums = df_all_nodes[df_all_nodes['Node Type'] == 'Album'][album_cols].copy().reset_index(drop=True)
    print(f"df_albums: {df_albums.shape}")
    df_albums.head()
    return (df_albums,)


@app.cell
def _(df_all_nodes):
    # Persons
    person_cols = ['id', 'name', 'stage_name']
    person_cols = [c for c in person_cols if c in df_all_nodes.columns]
    df_persons = df_all_nodes[df_all_nodes['Node Type'] == 'Person'][person_cols].copy().reset_index(drop=True)
    print(f"df_persons: {df_persons.shape}")
    df_persons.head()
    return (df_persons,)


@app.cell
def _(df_all_nodes):
    # Musical Groups
    df_groups = df_all_nodes[df_all_nodes['Node Type'] == 'MusicalGroup'][['id', 'name']].copy().reset_index(drop=True)
    print(f"df_groups: {df_groups.shape}")
    df_groups.head()
    return (df_groups,)


@app.cell
def _(df_all_nodes):
    # Record Labels
    df_labels = df_all_nodes[df_all_nodes['Node Type'] == 'RecordLabel'][['id', 'name']].copy().reset_index(drop=True)
    print(f"df_labels: {df_labels.shape}")
    df_labels.head()
    return (df_labels,)


@app.cell
def _(mo):
    mo.md(r"""
    ## Edge-Enriched Tables
    """)
    return


@app.cell
def _(df_all_edges, id_to_type):
    # Resolve source/target types on edges for filtering
    df_all_edges['source_type'] = df_all_edges['source'].map(id_to_type)
    df_all_edges['target_type'] = df_all_edges['target'].map(id_to_type)

    def agg_incoming(edge_type, node_ids, source_type=None):
        """Aggregate incoming edges (other -> node) as lists, optionally filtered by source type."""
        mask = (df_all_edges['Edge Type'] == edge_type) & (df_all_edges['target'].isin(node_ids))
        if source_type:
            mask = mask & (df_all_edges['source_type'] == source_type)
        subset = df_all_edges[mask]
        return subset.groupby('target')['source_name'].apply(list)

    def agg_outgoing(edge_type, node_ids, target_type=None):
        """Aggregate outgoing edges (node -> other) as lists, optionally filtered by target type."""
        mask = (df_all_edges['Edge Type'] == edge_type) & (df_all_edges['source'].isin(node_ids))
        if target_type:
            mask = mask & (df_all_edges['target_type'] == target_type)
        subset = df_all_edges[mask]
        return subset.groupby('source')['target_name'].apply(list)
    return agg_incoming, agg_outgoing


@app.cell
def _(agg_incoming, agg_outgoing, df_songs):
    # Song edge table — every source/target type gets its own column per the PDF schema
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
    df_song_edges.head()
    return


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
    df_album_edges.head()
    return


@app.cell
def _(agg_incoming, agg_outgoing, df_persons):
    # Person edge table — split by every possible target type per the PDF schema
    person_ids = set(df_persons['id'])
    df_person_edges = df_persons.copy()

    # PerformerOf: Person -> Song or Album
    df_person_edges['performer_of_songs']  = df_person_edges['id'].map(agg_outgoing('PerformerOf', person_ids, 'Song'))
    df_person_edges['performer_of_albums'] = df_person_edges['id'].map(agg_outgoing('PerformerOf', person_ids, 'Album'))

    # ComposerOf: Person -> Song or Album
    df_person_edges['composer_of_songs']  = df_person_edges['id'].map(agg_outgoing('ComposerOf', person_ids, 'Song'))
    df_person_edges['composer_of_albums'] = df_person_edges['id'].map(agg_outgoing('ComposerOf', person_ids, 'Album'))

    # ProducerOf: Person -> Song, Album, Person, or MusicalGroup
    df_person_edges['producer_of_songs']   = df_person_edges['id'].map(agg_outgoing('ProducerOf', person_ids, 'Song'))
    df_person_edges['producer_of_albums']  = df_person_edges['id'].map(agg_outgoing('ProducerOf', person_ids, 'Album'))
    df_person_edges['producer_of_persons'] = df_person_edges['id'].map(agg_outgoing('ProducerOf', person_ids, 'Person'))
    df_person_edges['producer_of_groups']  = df_person_edges['id'].map(agg_outgoing('ProducerOf', person_ids, 'MusicalGroup'))

    # LyricistOf: Person -> Song or Album
    df_person_edges['lyricist_of_songs']  = df_person_edges['id'].map(agg_outgoing('LyricistOf', person_ids, 'Song'))
    df_person_edges['lyricist_of_albums'] = df_person_edges['id'].map(agg_outgoing('LyricistOf', person_ids, 'Album'))

    # MemberOf: Person -> MusicalGroup
    df_person_edges['member_of'] = df_person_edges['id'].map(agg_outgoing('MemberOf', person_ids, 'MusicalGroup'))

    # Incoming: Person can be produced by another Person or RecordLabel
    df_person_edges['produced_by_persons'] = df_person_edges['id'].map(agg_incoming('ProducerOf', person_ids, 'Person'))
    df_person_edges['produced_by_labels']  = df_person_edges['id'].map(agg_incoming('ProducerOf', person_ids, 'RecordLabel'))

    print(f"df_person_edges: {df_person_edges.shape}")
    df_person_edges.head()
    return (df_person_edges,)


@app.cell
def _(agg_incoming, agg_outgoing, df_groups):
    # Musical Group edge table — split by every possible source/target type per the PDF schema
    group_ids = set(df_groups['id'])
    df_group_edges = df_groups.copy()

    # PerformerOf: MusicalGroup -> Song or Album
    df_group_edges['performer_of_songs']  = df_group_edges['id'].map(agg_outgoing('PerformerOf', group_ids, 'Song'))
    df_group_edges['performer_of_albums'] = df_group_edges['id'].map(agg_outgoing('PerformerOf', group_ids, 'Album'))

    # Incoming MemberOf: Person -> MusicalGroup
    df_group_edges['members'] = df_group_edges['id'].map(agg_incoming('MemberOf', group_ids, 'Person'))

    # Incoming ProducerOf: Person or RecordLabel -> MusicalGroup
    df_group_edges['produced_by_persons'] = df_group_edges['id'].map(agg_incoming('ProducerOf', group_ids, 'Person'))
    df_group_edges['produced_by_labels']  = df_group_edges['id'].map(agg_incoming('ProducerOf', group_ids, 'RecordLabel'))

    print(f"df_group_edges: {df_group_edges.shape}")
    df_group_edges.head()
    return


@app.cell
def _(agg_incoming, agg_outgoing, df_labels):
    # Record Label edge table — split by every possible source/target type per the PDF schema
    label_ids = set(df_labels['id'])
    df_label_edges = df_labels.copy()

    # Incoming RecordedBy: Song or Album -> RecordLabel (split by source type)
    df_label_edges['recorded_songs']  = df_label_edges['id'].map(agg_incoming('RecordedBy', label_ids, 'Song'))
    df_label_edges['recorded_albums'] = df_label_edges['id'].map(agg_incoming('RecordedBy', label_ids, 'Album'))

    # Incoming DistributedBy: Song or Album -> RecordLabel (split by source type)
    df_label_edges['distributed_songs']  = df_label_edges['id'].map(agg_incoming('DistributedBy', label_ids, 'Song'))
    df_label_edges['distributed_albums'] = df_label_edges['id'].map(agg_incoming('DistributedBy', label_ids, 'Album'))

    # ProducerOf: RecordLabel -> Song, Album, Person, or MusicalGroup
    df_label_edges['producer_of_songs']   = df_label_edges['id'].map(agg_outgoing('ProducerOf', label_ids, 'Song'))
    df_label_edges['producer_of_albums']  = df_label_edges['id'].map(agg_outgoing('ProducerOf', label_ids, 'Album'))
    df_label_edges['producer_of_persons'] = df_label_edges['id'].map(agg_outgoing('ProducerOf', label_ids, 'Person'))
    df_label_edges['producer_of_groups']  = df_label_edges['id'].map(agg_outgoing('ProducerOf', label_ids, 'MusicalGroup'))

    print(f"df_label_edges: {df_label_edges.shape}")
    df_label_edges.head()
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## Summary
    | Base Table | Edge Table | Edge Columns |
    |---|---|---|
    | `df_songs` | `df_song_edges` | performed_by_persons, performed_by_groups, composed_by, produced_by_persons, produced_by_labels, lyrics_by, recorded_by, distributed_by, in_style_of_songs/albums/persons/groups, interpolates_from_songs/albums, cover_of_songs/albums, lyrical_ref_to_songs/albums, directly_samples_songs/albums |
    | `df_albums` | `df_album_edges` | Same 20 edge columns as songs |
    | `df_persons` | `df_person_edges` | performer_of_songs/albums, composer_of_songs/albums, producer_of_songs/albums/persons/groups, lyricist_of_songs/albums, member_of, produced_by_persons/labels |
    | `df_groups` | `df_group_edges` | performer_of_songs/albums, members, produced_by_persons/labels |
    | `df_labels` | `df_label_edges` | recorded_songs/albums, distributed_songs/albums, producer_of_songs/albums/persons/groups |
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Question 1
    Design and develop visualizations and visual analytic tools that will allow Silas to explore and understand the profile of Sailor Shift’s career
    """)
    return


@app.cell
def _(df_person_edges):
    # Finding Sailor Shift node
    def find_sailor(df_person_edges):
        sailor_row = df_person_edges[df_person_edges['name'].str.contains('Sailor Shift', case = False, na=False)]
        sailor_id = sailor_row.iloc[0]['id']
        sailor_name = sailor_row.iloc[0]['name']
        return sailor_id, sailor_name

    sailor_id, sailor_name = find_sailor(df_person_edges)
    print(f"Found Sailor Shift: {sailor_name} (ID: {sailor_id})")
    return (sailor_id,)


@app.cell
def _(df_person_edges, pd, sailor_id):
    def sailor_group(df_person_edges, sailor_id, pd):
        # Identify Sailor
        sailor_person_edges = df_person_edges[df_person_edges['id'] == sailor_id]
        if sailor_person_edges.empty:
            return sailor_id, []

        # Extract groups Sailor is a member of
        groups = sailor_person_edges.iloc[0]['member_of']
        if pd.isna(groups):
            return sailor_id, []

        return groups

    groups = sailor_group(df_person_edges, sailor_id, pd)
    print(f"Sailor Shift's group(s): {groups}")
    return


@app.cell
def _(df_all_edges, df_all_nodes, df_songs, sailor_id):
    def get_sailor_songs(df_all_edges, df_all_nodes, df_songs, sailor_id):

        authorship_types = {'ComposerOf', 'PerformerOf', 'LyricistOf', 'ProducerOf'}
        song_id_set = set(df_songs['id'])

        # Songs Sailor is directly credited on 
        sailor_direct = df_all_edges[
            (df_all_edges['source'] == sailor_id) &
            (df_all_edges['Edge Type'].isin(authorship_types)) &
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
                (df_all_edges['Edge Type'].isin(authorship_types)) &
                (df_all_edges['target'].isin(song_id_set))
            ]['target']
            ivy_song_ids = set(ivy_songs)

        # Tag each song with its source
        all_song_ids = solo_song_ids | ivy_song_ids
        def tag(song_id):
            in_solo = song_id in solo_song_ids
            in_ivy = song_id in ivy_song_ids
            if in_solo and in_ivy:
                return 'both'
            if in_solo:
                return 'solo'
            return 'ivy_echos'

        # Build the output table from df_songs metadata
        df_sailor_songs = df_songs[df_songs['id'].isin(all_song_ids)].copy()
        df_sailor_songs['credit_type'] = df_sailor_songs['id'].map(tag)

        # Also attach Sailor's specific roles for solo/both songs
        role_map = sailor_direct.groupby('id')['role'].apply(list).to_dict()
        df_sailor_songs['sailor_roles'] = df_sailor_songs['id'].map(role_map)

        return all_song_ids, df_sailor_songs.sort_values('release_date').reset_index(drop=True)

    all_song_ids, df_sailor_songs = get_sailor_songs(df_all_edges, df_all_nodes, df_songs, sailor_id)

    print(f"Total songs: {len(df_sailor_songs)}")
    print(df_sailor_songs['credit_type'].value_counts().to_string())
    df_sailor_songs.head(10)
    return (all_song_ids,)


@app.cell
def _(df_albums, df_all_edges, df_all_nodes, sailor_id):
    def get_sailor_albums(df_all_edges, df_all_nodes, df_album, sailor_id):

        authorship_types = {'ComposerOf', 'PerformerOf', 'LyricistOf', 'ProducerOf'}
        album_id_set = set(df_albums['id'])

        # Albums Sailor is directly credited on
        sailor_direct = df_all_edges[
            (df_all_edges['source'] == sailor_id) &
            (df_all_edges['Edge Type'].isin(authorship_types)) &
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
                    (df_all_edges['Edge Type'].isin(authorship_types)) &
                    (df_all_edges['target'].isin(album_id_set))
                ]['target']
            )

        # Tag each album with its source
        all_album_ids = solo_album_ids | ivy_album_ids
        def tag(album_id):
            in_solo = album_id in solo_album_ids
            in_ivy  = album_id in ivy_album_ids
            if in_solo and in_ivy:
                return 'both'
            if in_solo:
                return 'solo'
            return 'ivy_echos'

        # Build the output table from df_albums metadata
        df_sailor_albums = df_albums[df_albums['id'].isin(all_album_ids)].copy()
        df_sailor_albums['credit_type'] = df_sailor_albums['id'].map(tag)

        # Also attach Sailor's specific roles for solo/both albums
        role_map = sailor_direct.groupby('id')['role'].apply(list).to_dict()
        df_sailor_albums['sailor_roles'] = df_sailor_albums['id'].map(role_map)

        return all_album_ids, ivy_echos_ids, df_sailor_albums.sort_values('release_date').reset_index(drop=True)

    all_album_ids, ivy_echos_ids, df_sailor_albums = get_sailor_albums(df_all_edges, df_all_nodes, df_albums, sailor_id)

    print(f"Total albums: {len(df_sailor_albums)}")
    print(df_sailor_albums['credit_type'].value_counts().to_string())
    df_sailor_albums.head(10)
    return all_album_ids, ivy_echos_ids


@app.cell
def _(
    all_album_ids,
    all_song_ids,
    df_all_edges,
    df_all_nodes,
    ivy_echos_ids,
    pd,
    sailor_id,
):
    def build_influence_edges(sailor_work_ids, sailor_entity_ids, df_all_edges, df_all_nodes):

        influence_types = {'InStyleOf', 'InterpolatesFrom', 'CoverOf', 'DirectlySamples', 'LyricalReferenceTo'}

        # Year lookup from release_date across all nodes
        year_lookup   = (
            df_all_nodes.set_index('id')['release_date']
            .dropna().astype(str).str[:4]
            .apply(pd.to_numeric, errors='coerce').dropna().astype(int).to_dict()
        )

        # Finding influence to Sailor — target is what influenced her
        to_sailor = df_all_edges[
            (df_all_edges['source'].isin(sailor_work_ids)) &
            (df_all_edges['Edge Type'].isin(influence_types))
        ].copy()
        to_sailor['direction'] = 'to_sailor'

        # Another work influences Sailor — she is the target
        from_sailor = df_all_edges[
            (
                df_all_edges['target'].isin(sailor_work_ids) |
                df_all_edges['target'].isin(sailor_entity_ids)
            ) &
            (df_all_edges['Edge Type'].isin(influence_types))
        ].copy()
        from_sailor['direction'] = 'from_sailor'

        df_influence_edges = (
            pd.concat([to_sailor, from_sailor], ignore_index=True)
            .rename(columns={
                'source':      'source_id',
                'target':      'target_id',
                'source_name': 'source_name',
                'target_name': 'target_name',
                'source_type': 'source_node_type',
                'target_type': 'target_node_type',
                'Edge Type':   'edge_type',
            })
            [['source_id', 'source_name', 'source_node_type',
              'target_id', 'target_name', 'target_node_type',
              'edge_type', 'direction']]
            .copy()
        )

        df_influence_edges['year'] = df_influence_edges['source_id'].map(year_lookup)

        return df_influence_edges

    # Collect all Sailor's IDs 
    sailor_work_ids  = all_song_ids | all_album_ids
    sailor_entity_ids = {sailor_id} | ivy_echos_ids

    df_influence_edges = build_influence_edges(sailor_work_ids, sailor_entity_ids, df_all_edges, df_all_nodes)
    print(f"Total influence edges: {len(df_influence_edges)}")
    print(df_influence_edges['direction'].value_counts().to_string())
    df_influence_edges.head(10)
    return df_influence_edges, sailor_entity_ids


@app.cell
def _(df_all_edges, df_all_nodes, df_influence_edges, pd, sailor_entity_ids):
    def build_artist_influence(df_all_edges, df_all_nodes, df_influence_edges, sailor_entity_ids, pd):

        authorship_types = {'ComposerOf', 'PerformerOf', 'LyricistOf', 'ProducerOf'}
        person_types = {'Person', 'MusicalGroup'}
        work_types = {'Song', 'Album'}

        # genre lookup: Song/Album nodes carry genre; Person/Group/Label nodes will be NaN
        work_genre = df_all_nodes.set_index('id')['genre'].dropna().to_dict()

        # built from all authorship edges in the full graph
        auth = (
            df_all_edges[df_all_edges['Edge Type'].isin(authorship_types)]
            [['source', 'source_name', 'source_type', 'target', 'Edge Type']]
            .rename(columns={
                'source': 'artist_id',
                'source_name': 'artist_name',
                'source_type': 'artist_type',
                'target': 'work_id',
                'Edge Type': 'authorship_role',
            })
        )

        # to_sailor: another work/person/group is the source
        to_s = df_influence_edges[df_influence_edges['direction'] == 'to_sailor']

        direct_to = (
            to_s[to_s['target_node_type'].isin(person_types)]
            [['target_id', 'target_name', 'target_node_type', 'edge_type', 'direction', 'year']]
            .rename(columns={'target_id': 'artist_id', 'target_name': 'artist_name', 'target_node_type': 'artist_type'})
            .assign(authorship_role=None, via_work_id=None, via_work_name=None)
        )
        resolved_to = (
            to_s[to_s['target_node_type'].isin(work_types)]
            .merge(auth.rename(columns={'work_id': 'target_id'}), on='target_id', how='left')
            [['artist_id', 'artist_name', 'artist_type', 'authorship_role',
              'target_id', 'target_name', 'edge_type', 'direction', 'year']]
            .rename(columns={'target_id': 'via_work_id', 'target_name': 'via_work_name'})
        )

        # from_sailor: another work is the target
        from_s = df_influence_edges[df_influence_edges['direction'] == 'from_sailor']

        direct_from = (
            from_s[from_s['source_node_type'].isin(person_types)]
            [['source_id', 'source_name', 'source_node_type', 'edge_type', 'direction', 'year']]
            .rename(columns={'source_id': 'artist_id', 'source_name': 'artist_name', 'source_node_type': 'artist_type'})
            .assign(authorship_role=None, via_work_id=None, via_work_name=None)
        )
        resolved_from = (
            from_s[from_s['source_node_type'].isin(work_types)]
            .merge(auth.rename(columns={'work_id': 'source_id'}), on='source_id', how='left')
            [['artist_id', 'artist_name', 'artist_type', 'authorship_role',
              'source_id', 'source_name', 'edge_type', 'direction', 'year']]
            .rename(columns={'source_id': 'via_work_id', 'source_name': 'via_work_name'})
        )

        combined = pd.concat([direct_to, resolved_to, direct_from, resolved_from], ignore_index=True)
        df_influence_artists = (
            combined[~combined['artist_id'].isin(sailor_entity_ids)]
            [['artist_id', 'artist_name', 'artist_type', 'authorship_role',
              'via_work_id', 'via_work_name', 'edge_type', 'direction', 'year']]
            .reset_index(drop=True)
        )

        # genre of the via_work — the song/album carrying the influence relationship
        df_influence_artists['genre'] = df_influence_artists['via_work_id'].map(work_genre)

        # notoriety of the via_work
        work_notable = (
            df_all_nodes.set_index('id')['notable'].to_dict()
            if 'notable' in df_all_nodes.columns else {}
        )
        work_notoriety_date = (
            df_all_nodes.set_index('id')['notoriety_date'].dropna().to_dict()
            if 'notoriety_date' in df_all_nodes.columns else {}
        )
        df_influence_artists['via_work_notable'] = df_influence_artists['via_work_id'].map(work_notable)
        df_influence_artists['via_work_notoriety_date'] = df_influence_artists['via_work_id'].map(work_notoriety_date)

        return df_influence_artists

    df_influence_artists = build_artist_influence(df_all_edges, df_all_nodes, df_influence_edges, sailor_entity_ids, pd)
    print(f"df_influence_artists: {df_influence_artists.shape}")
    print("\ndirection:\n",  df_influence_artists['direction'].value_counts().to_string())
    print("\nedge_type:\n",  df_influence_artists['edge_type'].value_counts().to_string())
    print("\nartist_type:\n", df_influence_artists['artist_type'].value_counts().to_string())
    print("\ntop to_sailor influencers:\n",
          df_influence_artists[df_influence_artists['direction'] == 'to_sailor']
          ['artist_name'].value_counts().head(10).to_string())
    df_influence_artists.head(10)
    return (df_influence_artists,)


@app.cell
def _(
    df_all_edges,
    df_all_nodes,
    df_influence_artists,
    pd,
    sailor_entity_ids,
    sailor_id,
):
    def build_network(df_all_nodes, df_all_edges, df_influence_artists, sailor_entity_ids, sailor_id):

        influence_types = {'InStyleOf', 'InterpolatesFrom', 'CoverOf', 'DirectlySamples', 'LyricalReferenceTo'}
        authorship_types = {'ComposerOf', 'PerformerOf', 'LyricistOf', 'ProducerOf'}
        person_types = {'Person', 'MusicalGroup'}
        work_types = {'Song', 'Album'}

        # For work to artist mapping
        auth_df = (
            df_all_edges[df_all_edges['Edge Type'].isin(authorship_types)]
            [['source', 'target']].rename(columns={'source': 'artist_id', 'target': 'work_id'})
        )
        artist_to_works = auth_df.groupby('artist_id')['work_id'].apply(set).to_dict()

        # Getting all influence edges for hop2 later on
        all_inf = df_all_edges[df_all_edges['Edge Type'].isin(influence_types)]

        # Defining the first hop to/from Sailor from df_influence artists
        hop1_to   = set(df_influence_artists[df_influence_artists['direction'] == 'to_sailor']['artist_id'].dropna()) - sailor_entity_ids
        hop1_from = set(df_influence_artists[df_influence_artists['direction'] == 'from_sailor']['artist_id'].dropna()) - sailor_entity_ids

        # Getting the indirect influence Sailor has through the second hop (who influenced the artists that influenced her and vice versa)
        # First collecting the works owned by the hop1_to artists
        hop1_to_works = set().union(*[artist_to_works.get(a, set()) for a in hop1_to]) if hop1_to else set()
        # Who influenced the hop1 artists?
        h2_to_raw = all_inf[all_inf['target'].isin(hop1_to_works)].copy()
        h2_to_artist = h2_to_raw[h2_to_raw['source_type'].isin(person_types)][['source']].rename(columns={'source': 'hop2_artist'})
        h2_to_work   = (
            h2_to_raw[h2_to_raw['source_type'].isin(work_types)]
            .merge(auth_df.rename(columns={'work_id': 'source', 'artist_id': 'hop2_artist'}), on='source', how='left')
            [['hop2_artist']]
        )
        hop2_to = (
            pd.concat([h2_to_artist, h2_to_work])['hop2_artist']
            .dropna().unique()
        )
        hop2_to = set(hop2_to) - sailor_entity_ids - hop1_to - hop1_from

        # Now doing the same but for the opposite direction: who was influenced by the hop1_from artists?
        hop1_from_works = set().union(*[artist_to_works.get(a, set()) for a in hop1_from]) if hop1_from else set()
        h2_from_raw = all_inf[all_inf['source'].isin(hop1_from_works)].copy()
        h2_from_artist = h2_from_raw[h2_from_raw['target_type'].isin(person_types)][['target']].rename(columns={'target': 'hop2_artist'})
        h2_from_work = (
            h2_from_raw[h2_from_raw['target_type'].isin(work_types)]
            .merge(auth_df.rename(columns={'work_id': 'target', 'artist_id': 'hop2_artist'}), on='target', how='left')
            [['hop2_artist']]
        )
        hop2_from = (
            pd.concat([h2_from_artist, h2_from_work])['hop2_artist']
            .dropna().unique()
        )
        hop2_from = set(hop2_from) - sailor_entity_ids - hop1_to - hop1_from 

        # primary_genre per artist: mode of genres across all their works
        work_genre = df_all_nodes.set_index('id')['genre'].dropna().to_dict()
        def primary_genre(artist_id):
            works = artist_to_works.get(artist_id, set())
            genres = [work_genre[w] for w in works if w in work_genre]
            if not genres:
                return None
            from collections import Counter
            return Counter(genres).most_common(1)[0][0]

        # notable_work_count per artist: how many of their works are flagged as notable
        notable_works = set(
            df_all_nodes.loc[df_all_nodes['notable'] == True, 'id']
        ) if 'notable' in df_all_nodes.columns else set()
        def notable_count(artist_id):
            return len(artist_to_works.get(artist_id, set()) & notable_works)

        # Creating flat edge list
        id_to_name = df_all_nodes.set_index('id')['name'].to_dict()
        id_to_type = df_all_nodes.set_index('id')['Node Type'].to_dict()
        year_lookup = (
            df_all_nodes.set_index('id')['release_date']
            .dropna().astype(str).str[:4]
            .apply(pd.to_numeric, errors='coerce').dropna().astype(int).to_dict()
        )

        hop1_edges = df_influence_artists.copy()
        hop1_edges['hop'] = 1

        def make_hop2_rows(artist_ids, direction):
            rows = []
            for aid in artist_ids:
                rows.append({
                    'artist_id': aid,
                    'artist_name': id_to_name.get(aid),
                    'artist_type': id_to_type.get(aid),
                    'authorship_role': None,
                    'via_work_id': None,
                    'via_work_name': None,
                    'edge_type': None,
                    'direction': direction,
                    'year': None,
                    'hop': 2,
                })
            return pd.DataFrame(rows)

        hop2_to_rows   = make_hop2_rows(hop2_to,   'to_sailor')
        hop2_from_rows = make_hop2_rows(hop2_from, 'from_sailor')

        shared_cols = ['artist_id', 'artist_name', 'artist_type', 'authorship_role',
                       'via_work_id', 'via_work_name', 'edge_type', 'direction', 'year', 'hop']

        df_network_edges = pd.concat(
            [hop1_edges[shared_cols], hop2_to_rows[shared_cols], hop2_from_rows[shared_cols]],
            ignore_index=True
        )
        df_network_edges = df_network_edges[~df_network_edges['artist_id'].isin(sailor_entity_ids)].copy()
        df_network_edges['primary_genre']      = df_network_edges['artist_id'].map(primary_genre)
        df_network_edges['notable_work_count'] = df_network_edges['artist_id'].map(notable_count)

        # node table: one row per unique artist
        df_network_nodes = (
            df_network_edges[['artist_id', 'artist_name', 'artist_type', 'primary_genre', 'notable_work_count']]
            .drop_duplicates(subset='artist_id')
            .reset_index(drop=True)
        )
        hop_label = (
            df_network_edges.groupby('artist_id')['hop'].min()
            .rename('min_hop').reset_index()
        )
        df_network_nodes = df_network_nodes.merge(hop_label, on='artist_id', how='left')

        return df_network_edges, df_network_nodes

    df_network_edges, df_network_nodes = build_network(df_all_nodes, df_all_edges, df_influence_artists, sailor_entity_ids, sailor_id)

    print(f"df_network_edges: {df_network_edges.shape}")
    print("\nhop:\n",       df_network_edges['hop'].value_counts().to_string())
    print("\ndirection:\n", df_network_edges['direction'].value_counts().to_string())
    print(f"\ndf_network_nodes: {df_network_nodes.shape}")
    df_network_edges.head(10)
    return df_network_edges, df_network_nodes


if __name__ == "__main__":
    app.run()
