// Probe: copies Ferrite's hash_content_bytes (src/markdown/csv_viewer.rs:615-625),
// which gates re-parsing of the cached CSV model (1633-1634, 1703) that cell
// edits serialize back over tab.content (apply_pending_cell_commit, 1115-1131).
use std::collections::hash_map::DefaultHasher;
use std::hash::{Hash, Hasher};

fn hash_content_bytes(content: &[u8]) -> u64 {
    let mut hasher = DefaultHasher::new();
    content.len().hash(&mut hasher);
    if content.len() > 8192 {
        content[..4096].hash(&mut hasher);
        content[content.len() - 4096..].hash(&mut hasher);
    } else {
        content.hash(&mut hasher);
    }
    hasher.finish()
}

fn main() {
    // ~40 KB CSV (well under the 1 MB editing gate).
    let mut csv = String::from("id,qty\n");
    for i in 0..4000 { csv.push_str(&format!("{:04},10\n", i)); }
    let before = hash_content_bytes(csv.as_bytes());

    // User edits row 2000's qty 10 -> 99 in Raw view (same length, mid-file).
    let row = "2000,10\n";
    let pos = csv.find(row).unwrap();
    let mut edited = csv.clone();
    edited.replace_range(pos..pos + row.len(), "2000,99\n");
    let after = hash_content_bytes(edited.as_bytes());

    println!("len {} -> {}, pos {} of {}", csv.len(), edited.len(), pos, csv.len());
    println!("sampled hash equal after mid-file edit: {}", before == after);
    println!("=> needs_rebuild = false; cached rows still say qty=10; the next cell commit serializes them over tab.content");
}
