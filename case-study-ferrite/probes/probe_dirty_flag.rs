// Probe: copies the bodies of Ferrite's Tab::is_modified / is_modified_cached /
// is_modified_uncached (src/state.rs:1984-2016), prepare_undo_snapshot_hashed
// (2595-2609), record_edit_from_snapshot_inner (2648-2662) and the legacy
// record_edit shim (2666-2674). blake3 is swapped for DefaultHasher and
// compute_edit_ops for a counter; neither changes the control flow.
// Sequence mirrors Duplicate Line (src/app/line_ops.rs:137,148) followed by the
// next raw-editor frame (src/editor/widget.rs:470 then 833).
use std::collections::hash_map::DefaultHasher;
use std::hash::{Hash, Hasher};

fn h(s: &str) -> u64 { let mut x = DefaultHasher::new(); s.hash(&mut x); x.finish() }

struct Tab {
    content: String,
    original_content: String,
    content_version: u64,
    save_version: u64,
    cached_is_modified: bool,
    cached_is_modified_version: u64,
    cached_is_modified_save_version: u64,
    pending_undo_snapshot: Option<String>,
    undo_content_hash: u64,
    undo_ops: usize,
}

impl Tab {
    fn is_modified(&self) -> bool {
        if self.cached_is_modified_version == self.content_version
            && self.cached_is_modified_save_version == self.save_version
        { return self.cached_is_modified; }
        self.content != self.original_content
    }
    fn is_modified_cached(&mut self) -> bool {
        if self.cached_is_modified_version == self.content_version
            && self.cached_is_modified_save_version == self.save_version
        { return self.cached_is_modified; }
        let r = self.content != self.original_content;
        self.cached_is_modified = r;
        self.cached_is_modified_version = self.content_version;
        self.cached_is_modified_save_version = self.save_version;
        r
    }
    fn prepare_undo_snapshot_hashed(&mut self) {
        let hash = h(&self.content);
        if hash != self.undo_content_hash {
            self.pending_undo_snapshot = Some(self.content.clone());
            self.undo_content_hash = hash;
        } else if self.pending_undo_snapshot.is_none() {
            self.pending_undo_snapshot = Some(self.content.clone());
            self.undo_content_hash = hash;
        }
    }
    fn record_external_edit_from_snapshot(&mut self) {
        if let Some(mut old) = self.pending_undo_snapshot.take() {
            if old != self.content {
                self.undo_ops += 1;
                old.clone_from(&self.content);
                self.undo_content_hash = h(&self.content);
                self.content_version = self.content_version.wrapping_add(1);
            }
            self.pending_undo_snapshot = Some(old);
        }
    }
    // Legacy shim: records undo, never bumps content_version.
    fn record_edit(&mut self, old_content: String) {
        if old_content != self.content {
            self.undo_ops += 1;
            self.undo_content_hash = h(&self.content);
            self.pending_undo_snapshot = None;
        }
    }
}

fn main() {
    let text = "line one\nline two".to_string();
    let mut tab = Tab {
        content: text.clone(), original_content: text.clone(),
        content_version: 1, save_version: 0,
        cached_is_modified: false, cached_is_modified_version: 0, cached_is_modified_save_version: 0,
        pending_undo_snapshot: None, undo_content_hash: 0, undo_ops: 0,
    };
    // Frame 1: title bar reads the dirty flag (caches false).
    tab.prepare_undo_snapshot_hashed();
    println!("after open: is_modified={}", tab.is_modified_cached());

    // Ctrl+Shift+D: handle_duplicate_line writes tab.content then record_edit.
    let old = tab.content.clone();
    tab.content = "line one\nline one\nline two".to_string();
    tab.record_edit(old);

    // Frame 2: EditorWidget::show -> prepare (widget.rs:470), external sync makes
    // the rope dirty (FerriteEditor::set_content sets content_dirty), so the widget
    // calls record_external_edit_from_snapshot (widget.rs:833).
    tab.prepare_undo_snapshot_hashed();
    tab.record_external_edit_from_snapshot();

    println!("after duplicate line: content differs from disk = {}", tab.content != tab.original_content);
    println!("after duplicate line: is_modified() = {}  (title-bar *, close prompt, autosave, has_unsaved_content all read this)", tab.is_modified_cached());
    println!("undo ops recorded = {}", tab.undo_ops);
}
