// Probe: moving a category under a parent of the other type flips the moved
// category's income/expense type but leaves its own subcategories as they were.
// Transcribed from repo/backend/src/categories/categories.service.ts:
//   update()            lines 434-545 (the parentId / isIncome branch, lines 507-523)
//   updateDescendantTypes() lines 558-577
// The database is replaced by an in-memory Map; the control flow is unchanged.
const rows = new Map();
function seed(id, parentId, isIncome) { rows.set(id, { id, parentId, isIncome }); }
seed("salary", null, true);        // income top-level
seed("fees", null, false);         // expense top-level
seed("bank-fees", "fees", false);  // expense child of fees

function updateDescendantTypes(parentId, isIncome) {
  const children = [...rows.values()].filter((c) => c.parentId === parentId);
  for (const child of children) {
    child.isIncome = isIncome;
    updateDescendantTypes(child.id, isIncome);
  }
}

function update(id, updateCategoryDto) {
  const category = rows.get(id);
  const beforeData = { isIncome: category.isIncome, parentId: category.parentId };
  if (updateCategoryDto.parentId !== undefined)
    category.parentId = updateCategoryDto.parentId;
  if (category.parentId) {
    const parent = rows.get(category.parentId);
    category.isIncome = parent.isIncome;
  } else if (updateCategoryDto.isIncome !== undefined) {
    category.isIncome = updateCategoryDto.isIncome;
  }
  // save
  if (
    !category.parentId &&
    updateCategoryDto.isIncome !== undefined &&
    updateCategoryDto.isIncome !== beforeData.isIncome
  ) {
    updateDescendantTypes(id, category.isIncome);
  }
}

// The user drags "fees" (with its child "bank-fees") under "salary".
update("fees", { parentId: "salary" });
for (const r of rows.values()) console.log(`${r.id.padEnd(10)} parent=${String(r.parentId).padEnd(7)} isIncome=${r.isIncome}`);
