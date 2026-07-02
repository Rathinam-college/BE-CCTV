import os
import django
from django.conf import settings
from django.apps import apps

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

out = []
for app_name in ['cctv', 'maintenance', 'users']:
    try:
        app_config = apps.get_app_config(app_name)
    except LookupError:
        continue
    out.append(f"# App: {app_name.capitalize()}")
    for model in app_config.get_models():
        out.append(f"## Table: {model._meta.db_table} (Model: {model.__name__})")
        out.append("| Column Name | Type | Description |")
        out.append("|---|---|---|")
        for field in model._meta.fields:
            fk_info = ""
            if field.is_relation and field.related_model:
                fk_info = f" -> {field.related_model._meta.db_table}"
            out.append(f"| {field.column} | {field.get_internal_type()} | {fk_info} |")
        out.append("")

with open("schema_dump.md", "w") as f:
    f.write("\n".join(out))
print("Schema generated at schema_dump.md")
