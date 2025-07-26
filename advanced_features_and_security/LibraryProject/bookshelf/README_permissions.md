# Bookshelf App: Permissions & Groups Setup

## Custom Permissions

The `Book` model defines the following custom permissions:

- `can_view`: Can view books
- `can_create`: Can create books
- `can_edit`: Can edit books
- `can_delete`: Can delete books

## Groups

Three groups are used to manage access:

- **Editors**: `can_create`, `can_edit`
- **Viewers**: `can_view`
- **Admins**: `can_create`, `can_edit`, `can_delete`, `can_view`

## Setup Instructions

1. **Apply Migrations**
   Ensure your database is up to date:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```
2. **Create Groups and Assign Permissions**
   Run the management command:
   ```bash
   python manage.py setup_groups_permissions
   ```
3. **Assign Users to Groups**
   Use the Django admin site to add users to the appropriate groups.

## Enforcing Permissions in Views

Views are protected using the `@permission_required` decorator. Example:

```python
@permission_required('bookshelf.can_edit', raise_exception=True)
def book_can_edit(request, pk):
    ...
```

## Testing

- Log in as users in different groups and verify access to create, edit, delete, and view book actions.
- Users will receive a 403 Forbidden error if they lack the required permission.

---

For any issues, check the Django admin for group and permission assignments.
