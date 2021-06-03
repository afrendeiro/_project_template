#!/usr/bin/env python

"""
A module to provide the boilerplate needed for all the analysis.
"""

import json
import re
from functools import partial
from typing import List, Dict, Final

import numpy as np  # type: ignore[import]
import pandas as pd  # type: ignore[import]
import matplotlib  # type: ignore[import]
import matplotlib.pyplot as plt  # type: ignore[import]
import seaborn as sns  # type: ignore[import]

from imc import Project  # type: ignore[import]
from imc.types import Path, DataFrame  # type: ignore[import]


# Initialize project
prj = Project(Config.metadata_dir / "samples.csv")

# Filter channels and ROIs
channels = (
    prj.channel_labels.stack().drop_duplicates().reset_index(level=1, drop=True)
)
channels_exclude = channels.loc[
    channels.str.contains(r"^\d")
    | channels.str.contains("|".join(Config.channels_exclude_strings))
].tolist() + ["<EMPTY>(Sm152-In115)"]
channels_include = channels[~channels.isin(channels_exclude)]

for roi in prj.rois:
    roi.set_channel_exclude(channels_exclude)

for s in prj:
    s.rois = [r for r in s if r.name not in Config.roi_exclude_strings]


class Config:
    # constants
    channels_exclude_strings: Final[List[str]] = [
        "<EMPTY>",
        "190BCKG",
        "80ArAr",
        "129Xe",
    ]
    roi_exclude_strings: Final[List[str]] = []

    ## Major attributes to contrast when comparing observation groups
    attributes: Final[List[str]] = []

    roi_attributes: DataFrame
    sample_attributes: DataFrame

    figkws: Final[Dict] = dict(
        dpi=300, bbox_inches="tight", pad_inches=0, transparent=False
    )

    # directories
    metadata_dir: Final[Path] = Path("metadata")
    data_dir: Final[Path] = Path("data")
    processed_dir: Final[Path] = Path("processed")
    results_dir: Final[Path] = Path("results")

    # # Order
    cat_order: Final[Dict[str, List]] = dict(
        cat1=["val1", "val2"],
        cat2=["val1", "val2"],
    )

    # Color codes
    colors: Final[Dict[str, np.ndarray]] = dict(
        cat1=np.asarray(sns.color_palette())[[2, 0, 1, 3]],
        cat2=np.asarray(sns.color_palette())[[2, 0, 1, 5, 4, 3]],
    )

    # Output files
    metadata_file: Final[Path] = metadata_dir / "clinical_annotation.pq"
    quantification_file: Final[Path] = (
        results_dir / "cell_type" / "quantification.pq"
    )
    gating_file: Final[Path] = results_dir / "cell_type" / "gating.pq"
    h5ad_file: Final[Path] = (
        results_dir / "cell_type" / "anndata.all_cells.processed.h5ad"
    )
    counts_file: Final[Path] = results_dir / "cell_type" / "cell_type_counts.pq"
    roi_areas_file: Final[Path] = results_dir / "roi_areas.csv"
    sample_areas_file: Final[Path] = results_dir / "sample_areas.csv"


# # ROIs
roi_names = [x.name for x in prj.rois]
Config.roi_attributes = (
    pd.DataFrame(
        np.asarray(
            [
                getattr(r.sample, attr)
                for r in prj.rois
                for attr in Config.attributes
            ]
        ).reshape((-1, len(Config.attributes))),
        index=roi_names,
        columns=Config.attributes,
    )
    .rename_axis(index="roi")
    .rename(columns={"name": "sample"})
)


# # Samples
sample_names = [x.name for x in prj.samples]
Config.sample_attributes = (
    pd.DataFrame(
        np.asarray(
            [
                getattr(s, attr)
                for s in prj.samples
                for attr in Config.attributes
            ]
        ).reshape((-1, len(Config.attributes))),
        index=sample_names,
        columns=Config.attributes,
    )
    .rename_axis(index="sample")
    .drop(["name"], axis=1)
)

for df in [Config.roi_attributes, Config.sample_attributes]:
    for cat, order in Config.cat_order.items():
        df[cat] = pd.Categorical(df[cat], categories=order, ordered=True)

    # Change dtype of integers
    df["var1"] = df["var1"].astype(int)
