# Generated by Django 5.1.2 on 2024-10-23 23:21

import django.db.models.deletion
import pgtrigger.compiler
import pgtrigger.migrations
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0002_add_boards_and_keywords"),
        ("pghistory", "0006_delete_aggregateevent"),
    ]

    operations = [
        migrations.CreateModel(
            name="CommentContentEvent",
            fields=[
                ("pgh_id", models.AutoField(primary_key=True, serialize=False)),
                ("pgh_created_at", models.DateTimeField(auto_now_add=True)),
                ("pgh_label", models.TextField(help_text="The event label.")),
                ("content", models.TextField(max_length=10000)),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="PostTitleEvent",
            fields=[
                ("pgh_id", models.AutoField(primary_key=True, serialize=False)),
                ("pgh_created_at", models.DateTimeField(auto_now_add=True)),
                ("pgh_label", models.TextField(help_text="The event label.")),
                ("title", models.CharField(max_length=120)),
            ],
            options={
                "abstract": False,
            },
        ),
        pgtrigger.migrations.AddTrigger(
            model_name="comment",
            trigger=pgtrigger.compiler.Trigger(
                name="insert_insert",
                sql=pgtrigger.compiler.UpsertTriggerSql(
                    func='INSERT INTO "app_commentcontentevent" ("content", "pgh_context_id", "pgh_created_at", "pgh_label", "pgh_obj_id") VALUES (NEW."content", _pgh_attach_context(), NOW(), \'insert\', NEW."id"); RETURN NULL;',
                    hash="074f190b6b19719a27926437731e121216fa59d5",
                    operation="INSERT",
                    pgid="pgtrigger_insert_insert_4b534",
                    table="app_comment",
                    when="AFTER",
                ),
            ),
        ),
        pgtrigger.migrations.AddTrigger(
            model_name="comment",
            trigger=pgtrigger.compiler.Trigger(
                name="update_update",
                sql=pgtrigger.compiler.UpsertTriggerSql(
                    condition='WHEN (OLD."content" IS DISTINCT FROM (NEW."content"))',
                    func='INSERT INTO "app_commentcontentevent" ("content", "pgh_context_id", "pgh_created_at", "pgh_label", "pgh_obj_id") VALUES (NEW."content", _pgh_attach_context(), NOW(), \'update\', NEW."id"); RETURN NULL;',
                    hash="8baaec4184f94195e7b7a97bb54cc19de574469a",
                    operation="UPDATE",
                    pgid="pgtrigger_update_update_09a9e",
                    table="app_comment",
                    when="AFTER",
                ),
            ),
        ),
        pgtrigger.migrations.AddTrigger(
            model_name="post",
            trigger=pgtrigger.compiler.Trigger(
                name="insert_insert",
                sql=pgtrigger.compiler.UpsertTriggerSql(
                    func='INSERT INTO "app_posttitleevent" ("pgh_context_id", "pgh_created_at", "pgh_label", "pgh_obj_id", "title") VALUES (_pgh_attach_context(), NOW(), \'insert\', NEW."id", NEW."title"); RETURN NULL;',
                    hash="f753980102ce1a3ab489827a1adf33bddfe16931",
                    operation="INSERT",
                    pgid="pgtrigger_insert_insert_c25c0",
                    table="app_post",
                    when="AFTER",
                ),
            ),
        ),
        pgtrigger.migrations.AddTrigger(
            model_name="post",
            trigger=pgtrigger.compiler.Trigger(
                name="update_update",
                sql=pgtrigger.compiler.UpsertTriggerSql(
                    condition='WHEN (OLD."title" IS DISTINCT FROM (NEW."title"))',
                    func='INSERT INTO "app_posttitleevent" ("pgh_context_id", "pgh_created_at", "pgh_label", "pgh_obj_id", "title") VALUES (_pgh_attach_context(), NOW(), \'update\', NEW."id", NEW."title"); RETURN NULL;',
                    hash="aff2486ab192ab2cf390a59666c6ca231ed855e4",
                    operation="UPDATE",
                    pgid="pgtrigger_update_update_99268",
                    table="app_post",
                    when="AFTER",
                ),
            ),
        ),
        migrations.AddField(
            model_name="commentcontentevent",
            name="pgh_context",
            field=models.ForeignKey(
                db_constraint=False,
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="+",
                to="pghistory.context",
            ),
        ),
        migrations.AddField(
            model_name="commentcontentevent",
            name="pgh_obj",
            field=models.ForeignKey(
                db_constraint=False,
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="content_events",
                to="app.comment",
            ),
        ),
        migrations.AddField(
            model_name="posttitleevent",
            name="pgh_context",
            field=models.ForeignKey(
                db_constraint=False,
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="+",
                to="pghistory.context",
            ),
        ),
        migrations.AddField(
            model_name="posttitleevent",
            name="pgh_obj",
            field=models.ForeignKey(
                db_constraint=False,
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="title_events",
                to="app.post",
            ),
        ),
    ]
