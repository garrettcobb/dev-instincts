// Copies the cursor arithmetic shared by handle_duplicate_line (line_ops.rs:79-153),
// handle_move_line (159-247) and handle_delete_line (251-352): a CHAR column from
// tab.cursor_position is added to a BYTE line start, then the String is sliced.
use std::panic;
fn cursor_char(new_lines: &[&str], new_line_num: usize, cursor_col: usize) -> usize {
    let new_content = new_lines.join("\n");
    let mut start = 0usize;
    for (i, l) in new_lines.iter().enumerate() { if i == new_line_num { break; } start += l.len() + 1; }
    let len = new_lines.get(new_line_num).map(|l| l.len()).unwrap_or(0);
    let b = start + cursor_col.min(len);
    new_content[..b.min(new_content.len())].chars().count()
}
fn run(name: &str, f: impl FnOnce() -> usize + panic::UnwindSafe) {
    match panic::catch_unwind(f) { Ok(v) => println!("{name}: ok ({v})"), Err(_) => println!("{name}: PANIC -> abort in release") }
}
fn main() {
    panic::set_hook(Box::new(|_| {}));
    // Duplicate: line 0 "你好", cursor after 你 (char col 1); new cursor on duplicated line 1.
    run("duplicate line on '你好' col 1", || cursor_char(&["你好", "你好"], 1, 1));
    // Delete: delete ASCII line 0 with cursor at col 1; cursor lands on next line "øl".
    run("delete line 'ab' col 1 above 'øl'", || cursor_char(&["øl"], 0, 1));
    // Move up: "first\nøa", cursor col 1 on line 1.
    run("move line up 'øa' col 1", || cursor_char(&["øa", "first"], 0, 1));
    run("ascii control", || cursor_char(&["abc", "abc"], 1, 1));
}
