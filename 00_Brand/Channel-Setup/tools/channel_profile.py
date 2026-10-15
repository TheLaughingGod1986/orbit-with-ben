"""Orbit With Ben's settings for the shared channel tools (studio core, Ben 15 Oct 2026: "unify HOS and OWB but keeping
their own rules"). Each repo keeps its own copy of this file; the tools that read it are identical in both."""

NAME = "Orbit With Ben"
HANDLE = "OrbitWithBen"
# Orbit at frame 0 of a Short is a Never (AGENTS.md); gate_shorts_open's visor detector finds him.
ROBOT_FRAME0_CHECK = True
ROBOT_NAME = "Orbit"
SHORTS_LOG = "could-orbit-survive/TEST_LOG.md"
SLUG = "orbit"
# gate_shorts_open: same opening background as a recent Short (block-SSIM, calibrated on the OWB library 6 Oct 2026).
BACKGROUND_SSIM_CHECK = True
