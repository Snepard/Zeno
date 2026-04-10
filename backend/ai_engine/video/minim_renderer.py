"""
minim_renderer.py  ·  AI Guruji Visual Engine
Every scene MUST render meaningful animations aligned with the concept.
Zero tolerance for blank/empty screens.
"""

import logging
import math
import textwrap
import numpy as np
from manim import *

logger = logging.getLogger(__name__)


# ─────────────────────────────── HELPERS ─────────────────────────────────────

def _safe(data: dict, key: str, fallback):
    """Safely get a value; return fallback if None or missing."""
    v = data.get(key)
    if v is None:
        return fallback
    if isinstance(fallback, list) and not isinstance(v, list):
        return fallback
    if isinstance(fallback, (int, float)) and not isinstance(v, (int, float)):
        return fallback
    return v or fallback


def _shorten(text: str, width: int = 35) -> str:
    return textwrap.shorten(str(text), width=width, placeholder="…")


# ─────────────────────────────── SCENE CLASS ─────────────────────────────────

class GenericSceneRenderer(Scene):
    """
    Routes each scene to the correct animator based on `visual_type`.
    Guarantees a visible, concept-driven animation for every route.
    """

    def __init__(self, scene_data: dict, **kwargs):
        self.d = scene_data
        super().__init__(**kwargs)

    # ── Entry point ──────────────────────────────────────────────────────────
    def construct(self):
        self.camera.background_color = "#06060F"
        duration = max(8, int(_safe(self.d, "duration", 15)))
        vtype    = str(_safe(self.d, "visual_type", "bullet")).lower().strip()

        # Subtle dot-grid  – NO constant axis lines
        dots = VGroup()
        for x in range(-8, 9, 2):
            for y in range(-5, 6, 2):
                d = Dot(point=[x * 0.9, y * 0.9, 0], radius=0.025, color="#1A2A4A", fill_opacity=0.7)
                dots.add(d)
        self.add(dots)

        # Heading at top
        heading = str(_safe(self.d, "heading", ""))
        if heading:
            h = Text(heading, font_size=44, weight=BOLD)
            h.set_color_by_gradient(PURPLE_B, TEAL_B)
            h.to_edge(UP, buff=0.35)
            self.play(Write(h, run_time=0.9))

        dispatch = {
            "graph":      self._graph,
            "equation":   self._equation,
            "flow":       self._flow,
            "diagram":    self._diagram,
            "comparison": self._comparison,
            "timeline":   self._timeline,
            "neural":     self._neural,
            "code":       self._code,
            "orbit":      self._orbit,
            "wave":       self._wave,
            "force":      self._force,
            "transform":  self._transform,
            "bullet":     self._bullet,
        }
        dispatch.get(vtype, self._concept_visual)(duration)

    # ── Hold helper ──────────────────────────────────────────────────────────
    def _hold(self, duration: int):
        elapsed = self.renderer.time
        self.wait(max(1.5, duration - elapsed))

    # ══════════════════════════ GRAPH ════════════════════════════════════════
    def _graph(self, duration: int):
        raw_pts = _safe(self.d, "data_points", [[0,0],[1,1],[2,3],[3,2],[4,5],[5,6]])
        pts = [[float(p[0]), float(p[1])] for p in raw_pts if len(p) >= 2]
        if len(pts) < 2:
            pts = [[i, i*i*0.3] for i in range(6)]

        xs = [p[0] for p in pts]
        ys = [p[1] for p in pts]
        x_max = max(xs) + 0.5
        y_max = max(ys) + 0.5

        ax = Axes(
            x_range=[0, x_max, max(1, x_max / 5)],
            y_range=[0, y_max, max(1, y_max / 5)],
            axis_config={"color": BLUE_B, "include_numbers": True, "font_size": 22},
            tips=True,
        ).scale(0.8).shift(DOWN * 0.3)

        x_lbl = Text(_safe(self.d, "x_axis", "X"), font_size=26, color=TEAL_A)
        y_lbl = Text(_safe(self.d, "y_axis", "Y"), font_size=26, color=TEAL_A)
        ax_labels = ax.get_axis_labels(x_label=x_lbl, y_label=y_lbl)
        self.play(Create(ax), Write(ax_labels), run_time=1.0)

        line = ax.plot_line_graph(xs, ys, line_color=GOLD, stroke_width=4, add_vertex_dots=False)
        self.play(Create(line, run_time=1.8))

        dots = VGroup(*[
            Dot(ax.coords_to_point(x, y), color=YELLOW, radius=0.13)
            for x, y in pts
        ])
        self.play(LaggedStart(*[GrowFromCenter(d) for d in dots], lag_ratio=0.15, run_time=1.2))
        self._hold(duration)

    # ══════════════════════════ EQUATION (term-by-term explanation) ═══════════
    def _equation(self, duration: int):
        eq_str = str(_safe(self.d, "equation", r"E = mc^2"))
        steps  = [str(s) for s in _safe(self.d, "steps", [])]

        # ── 1. Write the full equation large at top ──────────────────────────
        full_eq = MathTex(eq_str, font_size=82)
        full_eq.set_color_by_gradient(GOLD_A, TEAL_A)
        full_eq.move_to(UP * 2.3)
        glow_box = SurroundingRectangle(
            full_eq, color=TEAL_A, buff=0.35, corner_radius=0.2,
            stroke_width=2, stroke_opacity=0.7
        )
        self.play(Write(full_eq, run_time=2.0))
        self.play(Create(glow_box, run_time=0.5))

        # ── 2. Color-coded term explanations ────────────────────────────────
        term_colors = [YELLOW_A, BLUE_B, GREEN_B, RED_B, PURPLE_B, TEAL_B]
        explained   = VGroup()

        if steps:
            for i, step in enumerate(steps[:5]):
                col = term_colors[i % len(term_colors)]
                row = VGroup(
                    Square(side_length=0.28, color=col, fill_color=col, fill_opacity=0.85),
                    Text(str(step), font_size=30, color=WHITE)
                ).arrange(RIGHT, buff=0.4)
                explained.add(row)
            explained.arrange(DOWN, aligned_edge=LEFT, buff=0.55)
            explained.move_to(DOWN * 0.8)
            for row in explained:
                self.play(FadeIn(row, shift=UP * 0.25, run_time=0.55))
        else:
            hint = Text(
                "Each variable works together to describe this relationship.",
                font_size=28, color=LIGHT_GREY
            ).move_to(DOWN * 0.6)
            self.play(FadeIn(hint, run_time=0.8))

        # ── 3. Pulse the equation to emphasise it ───────────────────────────
        self.play(
            full_eq.animate.set_color(WHITE).scale(1.08),
            rate_func=there_and_back, run_time=0.9
        )
        self._hold(duration)


    # ══════════════════════════ FLOW ═════════════════════════════════════════
    def _flow(self, duration: int):
        steps = _safe(self.d, "steps", _safe(self.d, "elements", ["Input", "Process", "Decision", "Output"]))
        steps = [str(s) for s in steps[:6]]
        if len(steps) < 2:
            steps = ["Start", "Process", "End"]

        colors = [BLUE_D, TEAL_D, PURPLE_D, GREEN_D, GOLD_D, RED_D]
        boxes, labels = VGroup(), VGroup()

        for i, step in enumerate(steps):
            rect = RoundedRectangle(
                height=0.85, width=3.5,
                corner_radius=0.25,
                color=colors[i % len(colors)],
                fill_color=colors[i % len(colors)],
                fill_opacity=0.25,
                stroke_width=2,
            )
            txt = Text(_shorten(step, 30), font_size=27, color=WHITE)
            txt.move_to(rect.get_center())
            boxes.add(rect)
            labels.add(txt)

        boxes.arrange(DOWN, buff=0.65).scale(0.95).center().shift(DOWN * 0.2)
        for rect, lbl in zip(boxes, labels):
            lbl.move_to(rect.get_center())

        arrows = VGroup()
        for i in range(len(boxes) - 1):
            arr = Arrow(
                boxes[i].get_bottom(), boxes[i + 1].get_top(),
                buff=0.08, color=WHITE, stroke_width=2.5, max_tip_length_to_length_ratio=0.18,
            )
            arrows.add(arr)

        for rect, lbl in zip(boxes, labels):
            self.play(FadeIn(rect, shift=RIGHT * 0.3, run_time=0.4), Write(lbl, run_time=0.4))
        self.play(LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.25, run_time=1.0))
        self._hold(duration)

    # ══════════════════════════ DIAGRAM ══════════════════════════════════════
    def _diagram(self, duration: int):
        elements = [str(e) for e in _safe(self.d, "elements", ["A", "B", "C", "D"])][:6]
        lbls     = [str(l) for l in _safe(self.d, "labels", elements)]
        rels     = _safe(self.d, "relationships", [])
        n        = len(elements)
        palette  = [PURPLE_B, BLUE_C, TEAL_C, GREEN_C, GOLD_C, RED_C]

        node_map = {}
        all_mobs = VGroup()

        for i, el in enumerate(elements):
            angle = i * (2 * PI / n) - PI / 2
            pos   = RIGHT * 2.6 * math.cos(angle) + UP * 2.0 * math.sin(angle)
            circ  = Circle(radius=0.5, color=palette[i % len(palette)],
                           fill_color=palette[i % len(palette)], fill_opacity=0.3)
            circ.move_to(pos)
            lbl = Text(_shorten(lbls[i] if i < len(lbls) else el, 14),
                       font_size=22, color=WHITE)
            lbl.move_to(pos)
            node_map[el] = circ
            all_mobs.add(circ, lbl)

        edges = VGroup()
        for rel in rels:
            if len(rel) >= 2:
                a, b = str(rel[0]), str(rel[1])
                if a in node_map and b in node_map:
                    edges.add(Arrow(
                        node_map[a].get_center(), node_map[b].get_center(),
                        buff=0.5, color=TEAL_A, stroke_width=2, stroke_opacity=0.7,
                        max_tip_length_to_length_ratio=0.15,
                    ))

        if edges:
            self.play(Create(edges, run_time=1.0))
        self.play(LaggedStart(*[GrowFromCenter(m) for m in all_mobs], lag_ratio=0.1, run_time=1.5))
        self._hold(duration)

    # ══════════════════════════ COMPARISON ════════════════════════════════════
    def _comparison(self, duration: int):
        left_items  = [str(x) for x in _safe(self.d, "left_items",  ["Classical", "Deterministic", "Bit: 0 or 1"])]
        right_items = [str(x) for x in _safe(self.d, "right_items", ["Quantum", "Probabilistic", "Qubit: 0, 1, both"])]
        lbls        = [str(l) for l in _safe(self.d, "labels", ["A", "B"])]

        # Divider
        div = Line(UP * 3.2, DOWN * 3.2, color=GREY_B, stroke_width=1.5, stroke_opacity=0.5)
        self.play(Create(div, run_time=0.5))

        # Headers
        lh = Text(lbls[0] if lbls else "Left",  font_size=36, weight=BOLD, color=BLUE_B)
        rh = Text(lbls[1] if len(lbls) > 1 else "Right", font_size=36, weight=BOLD, color=GOLD_A)
        lh.move_to(LEFT * 3.2 + UP * 2.8)
        rh.move_to(RIGHT * 3.2 + UP * 2.8)

        # Decorative header bars
        lb = Underline(lh, color=BLUE_B)
        rb = Underline(rh, color=GOLD_A)
        self.play(Write(lh), Write(rh), Create(lb), Create(rb), run_time=0.8)

        pairs = list(zip(left_items[:5], right_items[:5]))
        for i, (l, r) in enumerate(pairs):
            y = 1.8 - i * 1.0
            li = VGroup(
                Dot(radius=0.1, color=BLUE_B),
                Text(_shorten(l, 28), font_size=27, color=LIGHT_GREY),
            ).arrange(RIGHT, buff=0.3).move_to(LEFT * 3.2 + UP * y)
            ri = VGroup(
                Dot(radius=0.1, color=GOLD_A),
                Text(_shorten(r, 28), font_size=27, color=LIGHT_GREY),
            ).arrange(RIGHT, buff=0.3).move_to(RIGHT * 3.2 + UP * y)
            self.play(FadeIn(li, shift=RIGHT * 0.3), FadeIn(ri, shift=LEFT * 0.3), run_time=0.5)

        self._hold(duration)

    # ══════════════════════════ TIMELINE ═════════════════════════════════════
    def _timeline(self, duration: int):
        steps = [str(s) for s in _safe(self.d, "steps", _safe(self.d, "elements", ["Phase 1", "Phase 2", "Phase 3"]))][:7]
        if not steps:
            steps = ["Start", "Middle", "End"]

        spine = Line(LEFT * 5.8, RIGHT * 5.8, color=TEAL_B, stroke_width=3)
        self.play(Create(spine, run_time=0.7))

        n = len(steps)
        for i, step in enumerate(steps):
            x = -5.0 + i * (10.0 / max(n - 1, 1))
            side = UP if i % 2 == 0 else DOWN
            dot  = Dot(RIGHT * x, color=GOLD, radius=0.2)
            tick = Line(RIGHT * x + UP * 0.25, RIGHT * x + DOWN * 0.25, color=GOLD, stroke_width=3)
            txt  = Text(_shorten(step, 16), font_size=22, color=WHITE)
            txt.move_to(RIGHT * x + side * 1.15)
            conn = DashedLine(RIGHT * x + side * 0.25, RIGHT * x + side * 0.85,
                              dash_length=0.1, color=TEAL_A, stroke_opacity=0.6)
            self.play(
                GrowFromCenter(dot), Create(tick),
                Create(conn), Write(txt),
                run_time=0.5,
            )
        self._hold(duration)

    # ══════════════════════════ NEURAL NETWORK ════════════════════════════════
    def _neural(self, duration: int):
        lbls = [str(l) for l in _safe(self.d, "labels", ["Input", "Hidden", "Output"])]
        sizes = [3, 4, 3][:len(lbls)]
        if not sizes:
            sizes = [3, 4, 3]
        palette = [BLUE_C, PURPLE_C, TEAL_C]

        layer_nodes = []
        all_nodes   = VGroup()

        for li, (sz, col) in enumerate(zip(sizes, palette)):
            x = -4.0 + li * 4.0
            col_group = VGroup()
            for ni in range(sz):
                y    = (ni - (sz - 1) / 2) * 1.3
                node = Circle(radius=0.38, color=col, fill_color=col, fill_opacity=0.25, stroke_width=2)
                node.move_to(RIGHT * x + UP * y)
                col_group.add(node)
            all_nodes.add(col_group)
            # Layer label
            lbl = Text(lbls[li] if li < len(lbls) else f"L{li}", font_size=26, color=WHITE)
            lbl.move_to(RIGHT * x + DOWN * 3.0)
            all_nodes.add(lbl)
            layer_nodes.append(col_group)

        self.play(LaggedStart(*[GrowFromCenter(m) for m in all_nodes], lag_ratio=0.07, run_time=1.5))

        # Weighted connections
        edges = VGroup()
        for i in range(len(layer_nodes) - 1):
            for src in layer_nodes[i]:
                for tgt in layer_nodes[i + 1]:
                    edges.add(Line(
                        src.get_center(), tgt.get_center(),
                        stroke_width=1.0, stroke_opacity=0.35, color=GREY_B,
                    ))
        self.play(Create(edges, run_time=1.2, lag_ratio=0.01))

        # Signal propagation sweep left → right
        for col_group in layer_nodes:
            self.play(
                LaggedStart(*[
                    Indicate(n, color=GOLD, scale_factor=1.4) for n in col_group
                ], lag_ratio=0.2, run_time=0.7),
            )
        self._hold(duration)

    # ══════════════════════════ CODE ═════════════════════════════════════════
    def _code(self, duration: int):
        lines = _safe(self.d, "steps", _safe(self.d, "bullets", ["# concept code", "print('Hello')"]))
        code_str = "\n".join(str(l) for l in lines[:12])
        if not code_str.strip():
            code_str = "# No code provided\nresult = concept(input)"

        panel = RoundedRectangle(
            width=12.5, height=6.5, corner_radius=0.35,
            color=GREY_D, fill_color="#12121E", fill_opacity=0.97,
        ).center().shift(DOWN * 0.3)
        self.play(FadeIn(panel, run_time=0.4))

        try:
            code_mob = Code(
                code=code_str,
                tab_width=4, background="window",
                language="Python", font="Monospace",
                font_size=26, line_spacing=1.3,
            ).scale_to_fit_width(11.5).center().shift(DOWN * 0.3)
            self.play(Write(code_mob, run_time=2.2))
        except Exception:
            # Fallback: plain text if Code() fails
            txt = Text(code_str, font_size=26, color=GREEN_A).center()
            self.play(Write(txt, run_time=1.5))

        self._hold(duration)

    # ══════════════════════════ ORBIT (Physics) ════════════════════════════════
    def _orbit(self, duration: int):
        """Physically animated orbital mechanics."""
        # Sun / central body
        sun = Dot(ORIGIN, radius=0.45, color=YELLOW)
        sun_glow = Circle(radius=0.55, color=GOLD_A, stroke_width=2, stroke_opacity=0.6)
        sun_label = Text("★ Central Body", font_size=24, color=YELLOW).next_to(sun, DOWN * 1.5)
        self.play(GrowFromCenter(sun), Create(sun_glow), Write(sun_label), run_time=0.8)

        # Orbit paths + planets
        radii  = [1.8, 2.8, 3.7]
        colors = [BLUE_C, TEAL_C, RED_C]
        plabels = _safe(self.d, "labels", ["Planet A", "Planet B", "Planet C"])

        orbits  = VGroup()
        planets = []
        for r, col, plbl in zip(radii, colors, plabels):
            orbit_circle = Circle(radius=r, color=col, stroke_opacity=0.3, stroke_width=1.5)
            planet = Dot(RIGHT * r, radius=0.22, color=col)
            planet_label = Text(_shorten(str(plbl), 14), font_size=20, color=col).next_to(planet, UR * 0.3)
            orbits.add(orbit_circle)
            planets.append((planet, planet_label, r, col))
            self.play(Create(orbit_circle), GrowFromCenter(planet), Write(planet_label), run_time=0.5)

        # Animate: each planet sweeps its orbit
        hold = max(2.0, (duration - self.renderer.time) / 2)
        for planet, lbl, r, col in planets:
            def make_updater(radius, label, phase=0.0):
                def updater(mob, dt, _phase=phase):
                    _phase += dt * (1.5 / radius)
                    mob.move_to(RIGHT * radius * math.cos(_phase) + UP * radius * math.sin(_phase))
                    label.next_to(mob, UR * 0.3)
                return updater
            planet.add_updater(make_updater(r, lbl))

        # Gravity force label
        eq = MathTex(r"F = \frac{Gm_1 m_2}{r^2}", font_size=42, color=WHITE)
        eq.to_corner(DR, buff=0.6)
        self.play(Write(eq, run_time=1.0))
        self.wait(hold)
        for planet, _, _, _ in planets:
            planet.clear_updaters()
        self._hold(duration)

    # ══════════════════════════ WAVE ══════════════════════════════════════════
    def _wave(self, duration: int):
        """Animated sine / concept wave."""
        ax = Axes(
            x_range=[0, 4 * PI, PI / 2],
            y_range=[-1.5, 1.5, 0.5],
            axis_config={"color": GREY_B, "include_numbers": False},
        ).scale(0.75).shift(DOWN * 0.3)
        self.play(Create(ax), run_time=0.8)

        t = ValueTracker(0)
        freq  = _safe(self.d, "data_points", [[1, 1]])[0][0] if _safe(self.d, "data_points", []) else 1

        wave = always_redraw(lambda: ax.plot(
            lambda x: np.sin(float(freq) * x - t.get_value()),
            x_range=[0, 4 * PI],
            color=TEAL_A,
            stroke_width=3,
        ))
        self.add(wave)

        # Labels
        labels = _safe(self.d, "labels", ["Sine Wave"])
        lbl = Text(_shorten(str(labels[0]), 30), font_size=28, color=TEAL_A).to_corner(DR, buff=0.6)
        self.play(Write(lbl, run_time=0.5))

        # Animate wave travelling
        travel_time = max(4.0, duration - self.renderer.time - 2.0)
        self.play(t.animate.set_value(3 * PI), run_time=travel_time, rate_func=linear)
        self._hold(duration)

    # ══════════════════════════ FORCE VECTORS ════════════════════════════════
    def _force(self, duration: int):
        """Arrows showing force, direction, and magnitude."""
        elements = [str(e) for e in _safe(self.d, "elements", ["Gravity", "Normal Force", "Friction"])]
        lbls     = [str(l) for l in _safe(self.d, "labels", elements)]
        rels     = _safe(self.d, "relationships", [])

        # Central object
        obj = Square(side_length=1.0, color=BLUE_B, fill_color=BLUE_E, fill_opacity=0.7)
        obj.center()
        obj_label = Text("Object", font_size=26, color=WHITE).move_to(obj.get_center())
        self.play(FadeIn(obj), Write(obj_label), run_time=0.6)

        # Arrow directions for each force
        directions = [DOWN * 2.2, UP * 2.2, LEFT * 2.5, RIGHT * 2.5, UR * 1.8, UL * 1.8]
        colors     = [GOLD, TEAL_A, RED_C, GREEN_C, PURPLE_A, BLUE_C]

        force_group = VGroup()
        for i, (el, lbl) in enumerate(zip(elements[:6], lbls + elements)):
            dir_vec = directions[i % len(directions)]
            arr = Arrow(
                obj.get_center(), obj.get_center() + dir_vec,
                color=colors[i % len(colors)], buff=0.5,
                stroke_width=4, max_tip_length_to_length_ratio=0.15,
            )
            force_lbl = Text(_shorten(lbl, 22), font_size=24, color=colors[i % len(colors)])
            force_lbl.next_to(arr.get_end(), arr.get_unit_vector() * 0.4)
            force_group.add(arr, force_lbl)

        self.play(LaggedStart(*[GrowArrow(a) if isinstance(a, Arrow) else Write(a)
                                for a in force_group], lag_ratio=0.2, run_time=1.5))

        # Pulsing object under forces
        self.play(obj.animate.set_fill(BLUE_C, opacity=0.9), run_time=0.5, rate_func=there_and_back)
        self._hold(duration)

    # ══════════════════════════ TRANSFORM ════════════════════════════════════
    def _transform(self, duration: int):
        """Shows a concept morphing / transforming into another."""
        steps = [str(s) for s in _safe(self.d, "steps", ["State A", "State B", "State C"])]
        colors = [BLUE_C, TEAL_C, GOLD_C, PURPLE_C, RED_C]

        if len(steps) < 2:
            steps = ["Before", "After"]

        shapes = []
        for i, step in enumerate(steps[:5]):
            col = colors[i % len(colors)]
            # Alternate between shapes to make the transforms visually dramatic
            mobs = [
                Circle(radius=1.4, color=col, fill_color=col, fill_opacity=0.3),
                RegularPolygon(n=3, radius=1.4, color=col, fill_color=col, fill_opacity=0.3),
                Square(side_length=2.8, color=col, fill_color=col, fill_opacity=0.3),
                RegularPolygon(n=6, radius=1.4, color=col, fill_color=col, fill_opacity=0.3),
                Star(outer_radius=1.4, color=col, fill_color=col, fill_opacity=0.3),
            ]
            shape = mobs[i % len(mobs)].center()
            txt   = Text(_shorten(step, 20), font_size=34, color=WHITE).center()
            shapes.append((shape, txt))

        # Show first shape
        cur_shape, cur_txt = shapes[0]
        self.play(GrowFromCenter(cur_shape), Write(cur_txt), run_time=0.8)

        for next_shape, next_txt in shapes[1:]:
            arrow_label = Text("→ transforms →", font_size=22, color=GREY_A)
            arrow_label.to_edge(DOWN, buff=0.5)
            self.play(Write(arrow_label, run_time=0.3))
            self.play(
                Transform(cur_shape, next_shape, run_time=1.2, rate_func=smooth),
                Transform(cur_txt, next_txt, run_time=1.0),
            )
            self.play(FadeOut(arrow_label, run_time=0.2))

        self._hold(duration)

    # ══════════════════════════ BULLET (last resort) ══════════════════════════
    def _bullet(self, duration: int):
        items = [str(b) for b in _safe(self.d, "bullets",
                    _safe(self.d, "elements",
                        _safe(self.d, "steps", ["No content available"])))][:7]
        group = VGroup()
        for b in items:
            dot = Dot(radius=0.13, color=TEAL, fill_opacity=0.9)
            txt = Text(_shorten(b, 55), font_size=31, color=LIGHT_GREY)
            row = VGroup(dot, txt).arrange(RIGHT, buff=0.45)
            group.add(row)
        group.arrange(DOWN, aligned_edge=LEFT, buff=0.65).center().shift(DOWN * 0.25)
        for row in group:
            self.play(FadeIn(row, shift=RIGHT * 0.4, run_time=0.55))
        self._hold(duration)

    # ══════════════════════════ CONCEPT VISUAL (auto-fallback) ════════════════
    def _concept_visual(self, duration: int):
        """
        Last-resort fallback: builds a rich animated visual from whatever
        data is available in self.d — no blank screens ever.
        """
        elements = [str(e) for e in _safe(self.d, "elements",
                        _safe(self.d, "steps",
                            _safe(self.d, "bullets", ["Concept"])))][:6]
        colors   = [BLUE_C, TEAL_C, GOLD_C, PURPLE_C, GREEN_C, RED_C]
        shapes   = VGroup()

        for i, el in enumerate(elements):
            angle = i * (2 * PI / max(len(elements), 1)) - PI / 2
            r     = 2.5
            pos   = RIGHT * r * math.cos(angle) + UP * r * math.sin(angle)
            circle = Circle(radius=0.55, color=colors[i % len(colors)],
                            fill_color=colors[i % len(colors)], fill_opacity=0.3)
            circle.move_to(pos)
            txt = Text(_shorten(el, 14), font_size=23, color=WHITE).move_to(pos)
            shapes.add(circle, txt)

        # Lines from center to each node
        lines = VGroup()
        for i in range(0, len(shapes), 2):
            node = shapes[i]
            lines.add(Line(ORIGIN, node.get_center(), color=GREY_B, stroke_opacity=0.4))

        hub = Dot(ORIGIN, radius=0.3, color=WHITE)
        self.play(Create(lines, run_time=0.8))
        self.play(GrowFromCenter(hub), run_time=0.4)
        self.play(LaggedStart(*[GrowFromCenter(m) for m in shapes], lag_ratio=0.1, run_time=1.5))
        self._hold(duration)


# ─────────────────────────────── PUBLIC API ───────────────────────────────────

def render_scene_with_minim(scene: dict, output_path: str, duration: int) -> str:
    """Renders a single conceptual scene using the Manim engine."""
    import os
    import shutil
    from pathlib import Path
    import imageio_ffmpeg

    scene["duration"] = max(8, duration)

    config.pixel_height      = 1080
    config.pixel_width       = 1920
    config.frame_rate        = 24
    config.ffmpeg_executable = imageio_ffmpeg.get_ffmpeg_exe()

    output_dir  = Path(output_path).parent
    base_name   = Path(output_path).stem

    config.media_dir   = str(output_dir)
    config.video_dir   = str(output_dir)
    config.format      = "mp4"
    config.output_file = base_name

    try:
        scene_instance = GenericSceneRenderer(scene)
        scene_instance.render()

        # Manim nests output in /videos/1080p24/ — flatten it out
        resolution_folder = "1080p24"
        generated = output_dir / "GenericSceneRenderer" / resolution_folder / f"{base_name}.mp4"
        if not generated.exists():
            generated = output_dir / resolution_folder / f"{base_name}.mp4"
        if generated.exists():
            shutil.move(str(generated), output_path)

        logger.info(f"Minim rendered: {output_path}")
        return output_path

    except Exception as e:
        logger.error(f"Minim/Manim failed to render scene: {e}")
        raise e
