// Probe: copies the cursor arithmetic of Ferrite's handle_move_line
// (src/app/line_ops.rs:159-247) and handle_duplicate_line (79-153).
// tab.cursor_position.1 is a CHAR column (src/editor/ferrite/cursor.rs:22,
// set from FerriteEditor at src/editor/widget.rs:849), but the code adds it
// to a BYTE offset and slices the String with it.
use std::panic;

fn move_line(content: &str, current_line_num: usize, cursor_col: usize, direction: isize) -> usize {
    let lines: Vec<&str> = content.split('\n').collect();
    let mut new_lines = lines.clone();
    if direction < 0 {
        new_lines.swap(current_line_num, current_line_num - 1);
    } else {
        new_lines.swap(current_line_num, current_line_num + 1);
    }
    let new_content = new_lines.join("\n");
    let new_line_num = if direction < 0 { current_line_num - 1 } else { current_line_num + 1 };
    let mut new_line_start = 0usize;
    for (i, line) in new_lines.iter().enumerate() {
        if i == new_line_num {
            break;
        }
        new_line_start += line.len() + 1;
    }
    let new_line_len = new_lines.get(new_line_num).map(|l| l.len()).unwrap_or(0);
    let new_cursor_byte = new_line_start + cursor_col.min(new_line_len);
    // line_ops.rs:216 -- same slice as the source
    new_content[..new_cursor_byte].chars().count()
}

fn main() {
    // ASCII: works.
    println!("ascii ok -> {}", move_line("first\nsecond", 1, 3, -1));
    // Line 1 is "øa"; cursor after 'ø' is char column 1 (byte 2). Alt+Up.
    let r = panic::catch_unwind(|| move_line("first\nøa", 1, 1, -1));
    match r {
        Ok(v) => println!("non-ascii -> {} (no panic)", v),
        Err(_) => println!("non-ascii -> PANIC (release build has panic = \"abort\": process exits)"),
    }
}
