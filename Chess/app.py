import streamlit as st
import sys
import os
import threading

sys.path.insert(0, os.path.dirname(__file__))
import ChessEngine
import AIEngine

# ─── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AIChess",
    page_icon="♟️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ─── CSS ──────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700;900&family=DM+Mono:wght@400;500&display=swap');

* { box-sizing: border-box; }

html, body, [data-testid="stAppViewContainer"] {
    background: #0d0d0d !important;
    color: #e8e0d0;
    font-family: 'DM Mono', monospace;
}

[data-testid="stAppViewContainer"] > .main {
    background: #0d0d0d !important;
}

[data-testid="block-container"] {
    padding: 1.5rem 2rem !important;
    max-width: 1200px;
}

h1 {
    font-family: 'Playfair Display', serif !important;
    font-size: 2.8rem !important;
    font-weight: 900 !important;
    letter-spacing: -1px;
    background: linear-gradient(135deg, #d4af37, #f5d76e, #c9982a);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0 !important;
}

.subtitle {
    color: #6b6560;
    font-size: 0.75rem;
    letter-spacing: 3px;
    text-transform: uppercase;
    margin-bottom: 1.5rem;
}

/* Buttons */
.stButton > button {
    background: transparent !important;
    border: 1px solid #3a3530 !important;
    color: #c9b99a !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 0.75rem !important;
    letter-spacing: 2px !important;
    text-transform: uppercase !important;
    padding: 0.5rem 1.2rem !important;
    border-radius: 2px !important;
    transition: all 0.2s !important;
    width: 100% !important;
}

.stButton > button:hover {
    background: #1e1a16 !important;
    border-color: #d4af37 !important;
    color: #d4af37 !important;
}

/* Radio */
[data-testid="stRadio"] > div {
    gap: 0.5rem;
}
[data-testid="stRadio"] label {
    color: #c9b99a !important;
    font-size: 0.8rem !important;
    font-family: 'DM Mono', monospace !important;
}

/* Move log panel */
.move-log-panel {
    background: #111008;
    border: 1px solid #2a2520;
    border-radius: 4px;
    padding: 1rem;
    height: 480px;
    overflow-y: auto;
    font-family: 'DM Mono', monospace;
    font-size: 0.75rem;
    color: #6b6560;
}

.move-log-panel::-webkit-scrollbar { width: 4px; }
.move-log-panel::-webkit-scrollbar-track { background: #0d0d0d; }
.move-log-panel::-webkit-scrollbar-thumb { background: #3a3530; }

.move-entry {
    display: flex;
    gap: 0.8rem;
    padding: 0.2rem 0;
    border-bottom: 1px solid #1a1510;
    color: #8a7f70;
}
.move-num { color: #4a4540; min-width: 24px; }
.move-w { color: #e8e0d0; }
.move-b { color: #8a7f70; }
.move-latest .move-w, .move-latest .move-b { color: #d4af37; }

/* Status banner */
.status-banner {
    background: #1a1510;
    border: 1px solid #3a3530;
    border-left: 3px solid #d4af37;
    padding: 0.6rem 1rem;
    font-size: 0.75rem;
    letter-spacing: 1px;
    color: #c9b99a;
    margin-bottom: 1rem;
    border-radius: 2px;
}

.status-check { border-left-color: #e85d4a; color: #e85d4a; }
.status-mate  { border-left-color: #d4af37; color: #d4af37; font-weight: bold; }

/* Section labels */
.section-label {
    font-size: 0.65rem;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: #4a4540;
    margin-bottom: 0.5rem;
    margin-top: 1rem;
}

/* Turn indicator */
.turn-indicator {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    font-size: 0.7rem;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: #8a7f70;
}
.turn-dot {
    width: 8px; height: 8px; border-radius: 50%;
}
.turn-dot.white { background: #e8e0d0; box-shadow: 0 0 6px rgba(232,224,208,0.4); }
.turn-dot.black { background: #2a2520; border: 1px solid #4a4540; }

/* Divider */
.gold-divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, #d4af37, transparent);
    margin: 1rem 0;
    opacity: 0.3;
}

/* Captured pieces */
.captured-row {
    font-size: 1rem;
    min-height: 1.5rem;
    letter-spacing: 2px;
}

/* AI thinking indicator */
.ai-thinking {
    color: #d4af37;
    font-size: 0.7rem;
    letter-spacing: 2px;
    animation: pulse 1.2s infinite;
}
@keyframes pulse { 0%,100%{opacity:1} 50%{opacity:0.3} }

[data-testid="stHorizontalBlock"] { gap: 1.5rem; }
</style>
""", unsafe_allow_html=True)

# ─── Piece unicode map ─────────────────────────────────────────────────────────
PIECE_UNICODE = {
    'wK': '♔', 'wQ': '♕', 'wR': '♖', 'wB': '♗', 'wN': '♘', 'wP': '♙',
    'bK': '♚', 'bQ': '♛', 'bR': '♜', 'bB': '♝', 'bN': '♞', 'bP': '♟',
}
PIECE_VALUE = {'Q': 9, 'R': 5, 'B': 3, 'N': 3, 'P': 1, 'K': 0}

# ─── Session state init ────────────────────────────────────────────────────────
def init_state():
    if 'gs' not in st.session_state:
        st.session_state.gs = ChessEngine.GameState()
        st.session_state.valid_moves = st.session_state.gs.getValidMoves()
        st.session_state.selected = None
        st.session_state.highlights = []
        st.session_state.game_mode = 'PvAI'   # 'PvAI' or 'PvP'
        st.session_state.player_color = 'w'    # human plays white
        st.session_state.game_over = False
        st.session_state.game_over_msg = ''
        st.session_state.move_log_display = []
        st.session_state.captured_w = []  # captured by white (black pieces lost)
        st.session_state.captured_b = []  # captured by black (white pieces lost)
        st.session_state.ai_thinking = False
        st.session_state.page = 'menu'    # 'menu' or 'game'

init_state()

# ─── Helpers ──────────────────────────────────────────────────────────────────
def reset_game():
    st.session_state.gs = ChessEngine.GameState()
    st.session_state.valid_moves = st.session_state.gs.getValidMoves()
    st.session_state.selected = None
    st.session_state.highlights = []
    st.session_state.game_over = False
    st.session_state.game_over_msg = ''
    st.session_state.move_log_display = []
    st.session_state.captured_w = []
    st.session_state.captured_b = []
    st.session_state.ai_thinking = False


def get_valid_move(start, end):
    move = ChessEngine.Move(start, end, st.session_state.gs.board)
    for vm in st.session_state.valid_moves:
        if move == vm:
            return vm
    return None


def get_highlights_for(row, col):
    return [(m.endRow, m.endCol) for m in st.session_state.valid_moves
            if m.startRow == row and m.startCol == col]


def update_captured(move):
    if move.pieceCaptured != '--':
        p = move.pieceCaptured
        if p[0] == 'b':
            st.session_state.captured_w.append(p)
        else:
            st.session_state.captured_b.append(p)


def do_move(move):
    gs = st.session_state.gs
    update_captured(move)
    gs.makeMove(move)
    st.session_state.valid_moves = gs.getValidMoves()
    # Update move log display
    log = gs.moveLog
    if len(log) % 2 == 1:
        st.session_state.move_log_display.append([str(log[-1]), ''])
    else:
        st.session_state.move_log_display[-1][1] = str(log[-1])
    # Check game over
    if gs.checkMate:
        winner = 'Black' if gs.whiteToMove else 'White'
        st.session_state.game_over = True
        st.session_state.game_over_msg = f'CHECKMATE — {winner} wins'
    elif gs.staleMate:
        st.session_state.game_over = True
        st.session_state.game_over_msg = 'STALEMATE — Draw'


def do_ai_move():
    gs = st.session_state.gs
    vm = st.session_state.valid_moves
    if not vm:
        return
    ai_move = AIEngine.findBestMove(gs, vm)
    if ai_move is None:
        ai_move = AIEngine.findRandomMove(vm)
    do_move(ai_move)


def undo_move():
    gs = st.session_state.gs
    if not gs.moveLog:
        return
    gs.undoMove()
    # If PvAI, undo twice (AI + human)
    if st.session_state.game_mode == 'PvAI' and gs.moveLog:
        gs.undoMove()
        if st.session_state.move_log_display:
            st.session_state.move_log_display.pop()
    if st.session_state.move_log_display:
        if st.session_state.move_log_display[-1][1] == '':
            st.session_state.move_log_display.pop()
        else:
            st.session_state.move_log_display[-1][1] = ''
    st.session_state.valid_moves = gs.getValidMoves()
    st.session_state.selected = None
    st.session_state.highlights = []
    st.session_state.game_over = False
    st.session_state.game_over_msg = ''
    # Rebuild captured from moveLog
    st.session_state.captured_w = []
    st.session_state.captured_b = []
    for m in gs.moveLog:
        if m.pieceCaptured != '--':
            p = m.pieceCaptured
            if p[0] == 'b':
                st.session_state.captured_w.append(p)
            else:
                st.session_state.captured_b.append(p)


# ─── SVG Board renderer ────────────────────────────────────────────────────────
def render_board_svg(gs, selected, highlights, valid_moves, flipped=False):
    SQ = 72
    BOARD = SQ * 8
    PAD_LEFT = 22
    PAD_BOTTOM = 22
    W = BOARD + PAD_LEFT
    H = BOARD + PAD_BOTTOM

    LIGHT = "#eeede9"
    DARK  = "#7c9155"
    SEL_COLOR   = "rgba(100,140,255,0.45)"
    HINT_COLOR  = "rgba(20,85,30,0.35)"
    LAST_COLOR  = "rgba(205,210,106,0.5)"
    CHECK_COLOR = "rgba(220,50,30,0.55)"

    svg = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
           f'viewBox="0 0 {W} {H}" style="display:block;margin:auto;border-radius:6px;'
           f'box-shadow:0 8px 40px rgba(0,0,0,0.7);">']

    # Background
    svg.append(f'<rect width="{W}" height="{H}" fill="#1a1510" rx="6"/>')

    # Last move highlight
    last_sq = set()
    if gs.moveLog:
        lm = gs.moveLog[-1]
        last_sq = {(lm.startRow, lm.startCol), (lm.endRow, lm.endCol)}

    # King in check
    check_sq = None
    if gs.inCheck():
        check_sq = gs.whiteKingLocation if gs.whiteToMove else gs.blackKingLocation

    for r in range(8):
        for c in range(8):
            dr = 7 - r if flipped else r
            dc = 7 - c if flipped else c

            base_color = LIGHT if (r + c) % 2 == 0 else DARK
            x = PAD_LEFT + dc * SQ
            y = dr * SQ

            svg.append(f'<rect x="{x}" y="{y}" width="{SQ}" height="{SQ}" fill="{base_color}"/>')

            # Last move overlay
            if (r, c) in last_sq:
                svg.append(f'<rect x="{x}" y="{y}" width="{SQ}" height="{SQ}" fill="{LAST_COLOR}"/>')

            # Selected square
            if selected == (r, c):
                svg.append(f'<rect x="{x}" y="{y}" width="{SQ}" height="{SQ}" fill="{SEL_COLOR}"/>')

            # King in check
            if check_sq == (r, c):
                svg.append(f'<rect x="{x}" y="{y}" width="{SQ}" height="{SQ}" fill="{CHECK_COLOR}" rx="2"/>')

            # Move hints
            if (r, c) in highlights:
                piece = gs.board[r][c]
                if piece != '--':
                    # Capture ring
                    svg.append(f'<rect x="{x}" y="{y}" width="{SQ}" height="{SQ}" '
                                f'fill="none" stroke="rgba(20,85,30,0.5)" stroke-width="5"/>')
                else:
                    # Dot
                    cx_dot = x + SQ // 2
                    cy_dot = y + SQ // 2
                    svg.append(f'<circle cx="{cx_dot}" cy="{cy_dot}" r="10" fill="{HINT_COLOR}"/>')

            # Piece
            piece = gs.board[r][c]
            if piece != '--':
                glyph = PIECE_UNICODE.get(piece, '?')
                px = x + SQ // 2
                py = y + SQ // 2 + 2
                # Shadow
                svg.append(f'<text x="{px+1}" y="{py+2}" text-anchor="middle" dominant-baseline="middle" '
                            f'font-size="42" fill="rgba(0,0,0,0.3)" font-family="serif">{glyph}</text>')
                # Piece
                fill = "#fafafa" if piece[0] == 'w' else "#1a1208"
                stroke = "#aaa" if piece[0] == 'w' else "#8a7f70"
                svg.append(f'<text x="{px}" y="{py}" text-anchor="middle" dominant-baseline="middle" '
                            f'font-size="42" fill="{fill}" stroke="{stroke}" stroke-width="0.5" '
                            f'font-family="serif">{glyph}</text>')

    # Rank labels (1–8)
    for r in range(8):
        dr = 7 - r if flipped else r
        label = str(8 - r) if not flipped else str(r + 1)
        y = dr * SQ + SQ // 2 + 5
        color = "#6b6560"
        svg.append(f'<text x="{PAD_LEFT - 5}" y="{y}" text-anchor="end" font-size="11" '
                   f'fill="{color}" font-family="DM Mono, monospace">{label}</text>')

    # File labels (a–h)
    files = "abcdefgh"
    for c in range(8):
        dc = 7 - c if flipped else c
        label = files[c] if not flipped else files[7 - c]
        x = PAD_LEFT + dc * SQ + SQ // 2
        y = BOARD + PAD_BOTTOM - 4
        color = "#6b6560"
        svg.append(f'<text x="{x}" y="{y}" text-anchor="middle" font-size="11" '
                   f'fill="{color}" font-family="DM Mono, monospace">{label}</text>')

    svg.append('</svg>')
    return ''.join(svg)


# ─── Clickable grid overlay ────────────────────────────────────────────────────
def render_click_buttons(flipped=False):
    cols = st.columns(8, gap="small")
    # We render 8 rows of 8 invisible buttons via st.columns trick
    # Actually we use a flat grid
    for r in range(8):
        row_cols = st.columns(8, gap="small")
        for c in range(8):
            br = 7 - r if flipped else r
            bc = 7 - c if flipped else c
            with row_cols[c]:
                label = f"{br},{bc}"
                if st.button("​", key=f"sq_{br}_{bc}", help=f"Row {br}, Col {bc}",
                             use_container_width=True):
                    handle_square_click(br, bc)


def handle_square_click(r, c):
    gs = st.session_state.gs
    if st.session_state.game_over:
        return

    # Determine if it's human's turn
    mode = st.session_state.game_mode
    if mode == 'PvAI':
        human_color = st.session_state.player_color
        is_human_turn = (gs.whiteToMove and human_color == 'w') or \
                        (not gs.whiteToMove and human_color == 'b')
        if not is_human_turn:
            return

    sel = st.session_state.selected
    piece = gs.board[r][c]

    if sel is None:
        # Select a piece of current player
        if piece != '--' and piece[0] == ('w' if gs.whiteToMove else 'b'):
            st.session_state.selected = (r, c)
            st.session_state.highlights = get_highlights_for(r, c)
    else:
        if (r, c) == sel:
            # Deselect
            st.session_state.selected = None
            st.session_state.highlights = []
        elif piece != '--' and piece[0] == ('w' if gs.whiteToMove else 'b'):
            # Switch selection to another own piece
            st.session_state.selected = (r, c)
            st.session_state.highlights = get_highlights_for(r, c)
        else:
            # Try to make move
            vm = get_valid_move(sel, (r, c))
            if vm:
                do_move(vm)
                st.session_state.selected = None
                st.session_state.highlights = []
                # Trigger AI if PvAI and not game over
                if mode == 'PvAI' and not st.session_state.game_over:
                    do_ai_move()
            else:
                st.session_state.selected = None
                st.session_state.highlights = []


# ─── Material advantage ───────────────────────────────────────────────────────
def material_advantage():
    w_val = sum(PIECE_VALUE.get(p[1], 0) for p in st.session_state.captured_w)
    b_val = sum(PIECE_VALUE.get(p[1], 0) for p in st.session_state.captured_b)
    return w_val - b_val


# ══════════════════════════════════════════════════════════════════════════════
# MENU PAGE
# ══════════════════════════════════════════════════════════════════════════════
def page_menu():
    st.markdown('<h1>AIChess</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Python · Minimax · Alpha-Beta Pruning</p>', unsafe_allow_html=True)
    st.markdown('<div class="gold-divider"></div>', unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1], gap="large")

    with col1:
        st.markdown('<p class="section-label">Game Mode</p>', unsafe_allow_html=True)
        mode = st.radio("", ["Player vs AI", "Player vs Player"], label_visibility="collapsed")

        if mode == "Player vs AI":
            st.markdown('<p class="section-label">Play as</p>', unsafe_allow_html=True)
            color = st.radio("", ["White ♔", "Black ♚"], label_visibility="collapsed")
            st.session_state.player_color = 'w' if color.startswith('White') else 'b'
            st.session_state.game_mode = 'PvAI'
        else:
            st.session_state.game_mode = 'PvP'

        st.markdown('<div style="margin-top:2rem"></div>', unsafe_allow_html=True)
        if st.button("START GAME", use_container_width=True):
            reset_game()
            st.session_state.page = 'game'
            # If PvAI and player is black, AI goes first
            if st.session_state.game_mode == 'PvAI' and st.session_state.player_color == 'b':
                do_ai_move()
            st.rerun()

    with col2:
        st.markdown("""
        <div style="background:#111008;border:1px solid #2a2520;padding:1.5rem;border-radius:4px;margin-top:1.5rem">
            <p style="font-size:0.65rem;letter-spacing:3px;color:#4a4540;text-transform:uppercase;margin-bottom:1rem">Features</p>
            <p style="font-size:0.8rem;color:#8a7f70;line-height:1.9">
                ♟ Full chess rules with castling & en passant<br>
                ♟ Pawn promotion to queen<br>
                ♟ Minimax + Alpha-Beta Pruning AI<br>
                ♟ Move ordering & transposition table<br>
                ♟ Depth-3 search (~20M nodes pruned)<br>
                ♟ Undo move support<br>
                ♟ Player vs Player mode
            </p>
        </div>
        """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# GAME PAGE
# ══════════════════════════════════════════════════════════════════════════════
def page_game():
    gs = st.session_state.gs

    # Flip board if player is black
    flipped = (st.session_state.game_mode == 'PvAI' and st.session_state.player_color == 'b')

    # ── Header ────────────────────────────────────────────────────────────────
    hcol1, hcol2 = st.columns([2, 1])
    with hcol1:
        st.markdown('<h1 style="font-size:1.8rem!important;margin-bottom:0">AIChess</h1>',
                    unsafe_allow_html=True)
    with hcol2:
        turn_color = "white" if gs.whiteToMove else "black"
        dot_class = "white" if gs.whiteToMove else "black"
        label = "White to move" if gs.whiteToMove else "Black to move"
        if st.session_state.game_mode == 'PvAI':
            hc = st.session_state.player_color
            is_human = (gs.whiteToMove and hc == 'w') or (not gs.whiteToMove and hc == 'b')
            label += " (You)" if is_human else " (AI)"
        st.markdown(
            f'<div style="margin-top:1rem" class="turn-indicator">'
            f'<div class="turn-dot {dot_class}"></div>{label}</div>',
            unsafe_allow_html=True)

    # ── Status banner ──────────────────────────────────────────────────────────
    if st.session_state.game_over:
        st.markdown(f'<div class="status-banner status-mate">⬛ {st.session_state.game_over_msg}</div>',
                    unsafe_allow_html=True)
    elif gs.inCheck():
        checked = "White" if gs.whiteToMove else "Black"
        st.markdown(f'<div class="status-banner status-check">⚠ {checked} is in check</div>',
                    unsafe_allow_html=True)

    # ── Main layout ────────────────────────────────────────────────────────────
    main_col, side_col = st.columns([5, 2], gap="large")

    with main_col:
        # Captured by black (white pieces lost) — shown above board
        cap_b = ' '.join(PIECE_UNICODE.get(p, '') for p in sorted(
            st.session_state.captured_b, key=lambda x: -PIECE_VALUE.get(x[1], 0)))
        adv = material_advantage()
        adv_str = f'+{adv}' if adv > 0 else (str(adv) if adv < 0 else '')
        st.markdown(
            f'<div style="display:flex;justify-content:space-between;align-items:center;'
            f'margin-bottom:4px;min-height:28px">'
            f'<span class="captured-row">{cap_b}</span>'
            f'<span style="font-size:0.7rem;color:#e85d4a">'
            f'{"−"+str(abs(adv)) if adv < 0 else ""}</span></div>',
            unsafe_allow_html=True)

        # Board SVG
        svg = render_board_svg(gs, st.session_state.selected,
                                set(st.session_state.highlights),
                                st.session_state.valid_moves, flipped)
        st.markdown(svg, unsafe_allow_html=True)

        # Captured by white (black pieces lost) — shown below board
        cap_w = ' '.join(PIECE_UNICODE.get(p, '') for p in sorted(
            st.session_state.captured_w, key=lambda x: -PIECE_VALUE.get(x[1], 0)))
        st.markdown(
            f'<div style="display:flex;justify-content:space-between;align-items:center;'
            f'margin-top:4px;min-height:28px">'
            f'<span class="captured-row">{cap_w}</span>'
            f'<span style="font-size:0.7rem;color:#6bbf6b">'
            f'{"+" + str(adv) if adv > 0 else ""}</span></div>',
            unsafe_allow_html=True)

        # ── Click grid ─────────────────────────────────────────────────────────
        st.markdown('<p class="section-label" style="margin-top:0.5rem">Click a square to select / move</p>',
                    unsafe_allow_html=True)

        if not st.session_state.game_over:
            for r in range(8):
                row_cols = st.columns(8, gap="small")
                for c in range(8):
                    br = 7 - r if flipped else r
                    bc = 7 - c if flipped else c
                    piece = gs.board[br][bc]
                    glyph = PIECE_UNICODE.get(piece, '·') if piece != '--' else '·'
                    is_sel = st.session_state.selected == (br, bc)
                    is_hint = (br, bc) in st.session_state.highlights
                    btn_style = ""
                    if is_sel:
                        btn_style = "background:#1e3a6e!important;border-color:#4a7fb5!important;"
                    elif is_hint:
                        btn_style = "background:#1e3a1e!important;border-color:#4a7f4a!important;"
                    with row_cols[c]:
                        if st.button(glyph, key=f"sq_{br}_{bc}",
                                     use_container_width=True):
                            handle_square_click(br, bc)
                            st.rerun()

    with side_col:
        # Controls
        st.markdown('<p class="section-label">Controls</p>', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            if st.button("↩ Undo", use_container_width=True):
                undo_move()
                st.rerun()
        with c2:
            if st.button("↺ Reset", use_container_width=True):
                reset_game()
                if st.session_state.game_mode == 'PvAI' and st.session_state.player_color == 'b':
                    do_ai_move()
                st.rerun()

        if st.button("⌂ Menu", use_container_width=True):
            st.session_state.page = 'menu'
            st.rerun()

        st.markdown('<div class="gold-divider"></div>', unsafe_allow_html=True)

        # Move log
        st.markdown('<p class="section-label">Move History</p>', unsafe_allow_html=True)
        log_html = ['<div class="move-log-panel">']
        entries = st.session_state.move_log_display
        for i, (mw, mb) in enumerate(entries):
            is_latest = (i == len(entries) - 1)
            cls = "move-entry move-latest" if is_latest else "move-entry"
            log_html.append(
                f'<div class="{cls}">'
                f'<span class="move-num">{i+1}.</span>'
                f'<span class="move-w">{mw}</span>'
                f'<span class="move-b">{mb}</span>'
                f'</div>')
        log_html.append('</div>')
        st.markdown(''.join(log_html), unsafe_allow_html=True)

        # Game info
        st.markdown('<div class="gold-divider"></div>', unsafe_allow_html=True)
        st.markdown('<p class="section-label">Info</p>', unsafe_allow_html=True)
        mode_label = "Player vs AI" if st.session_state.game_mode == 'PvAI' else "Player vs Player"
        total_moves = len(gs.moveLog)
        st.markdown(f"""
        <div style="font-size:0.7rem;color:#6b6560;line-height:2">
            Mode: <span style="color:#c9b99a">{mode_label}</span><br>
            Moves played: <span style="color:#c9b99a">{total_moves}</span><br>
            AI depth: <span style="color:#c9b99a">3</span><br>
            Algorithm: <span style="color:#c9b99a">NegaMax + α-β</span>
        </div>
        """, unsafe_allow_html=True)


# ─── Router ────────────────────────────────────────────────────────────────────
if st.session_state.page == 'menu':
    page_menu()
else:
    page_game()
