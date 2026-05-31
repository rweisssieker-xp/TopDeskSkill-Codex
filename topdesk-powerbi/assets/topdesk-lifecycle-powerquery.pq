// TOPdesk lifecycle import Power Query templates.
// Parameter expected: LifecycleImportRoot as text.
// Point it to the folder produced by sync_incident_lifecycle.py.

// Query name: FactIncidentDailySnapshot
let
    Source = Csv.Document(
        File.Contents(LifecycleImportRoot & "\incident_daily_snapshots.csv"),
        [Delimiter = ",", Encoding = 65001, QuoteStyle = QuoteStyle.Csv]
    ),
    PromotedHeaders = Table.PromoteHeaders(Source, [PromoteAllScalars = true]),
    Typed = Table.TransformColumnTypes(
        PromotedHeaders,
        {
            {"snapshot_date", type date},
            {"incident_id", type text},
            {"topdesk_id", type text},
            {"topdesk_number", type text},
            {"status_id", type text},
            {"status_name", type text},
            {"assigned_group_id", type text},
            {"assigned_group_name", type text},
            {"assigned_operator_id", type text},
            {"assigned_operator_name", type text},
            {"priority_id", type text},
            {"priority_name", type text},
            {"category_id", type text},
            {"category_name", type text},
            {"branch_id", type text},
            {"branch_name", type text},
            {"created_at", type datetimezone},
            {"modified_at", type datetimezone},
            {"target_at", type datetimezone},
            {"closed_at", type datetimezone},
            {"is_closed", type logical},
            {"snapshot_loaded_at", type datetimezone}
        }
    ),
    Renamed = Table.RenameColumns(
        Typed,
        {
            {"snapshot_date", "SnapshotDate"},
            {"incident_id", "IncidentKey"},
            {"topdesk_id", "TopdeskId"},
            {"topdesk_number", "TopdeskNumber"},
            {"status_id", "StatusId"},
            {"status_name", "StatusName"},
            {"assigned_group_id", "OperatorGroupId"},
            {"assigned_group_name", "OperatorGroupName"},
            {"assigned_operator_id", "OperatorId"},
            {"assigned_operator_name", "OperatorName"},
            {"priority_id", "PriorityId"},
            {"priority_name", "PriorityName"},
            {"category_id", "CategoryId"},
            {"category_name", "CategoryName"},
            {"branch_id", "BranchId"},
            {"branch_name", "BranchName"},
            {"created_at", "CreatedAt"},
            {"modified_at", "ModifiedAt"},
            {"target_at", "TargetAt"},
            {"closed_at", "ClosedAt"},
            {"is_closed", "IsClosed"},
            {"snapshot_loaded_at", "SnapshotLoadedAt"}
        }
    )
in
    Renamed

// Query name: FactStatusTransition
let
    Source = Csv.Document(
        File.Contents(LifecycleImportRoot & "\FactStatusTransition.csv"),
        [Delimiter = ",", Encoding = 65001, QuoteStyle = QuoteStyle.Csv]
    ),
    PromotedHeaders = Table.PromoteHeaders(Source, [PromoteAllScalars = true]),
    Typed = Table.TransformColumnTypes(
        PromotedHeaders,
        {
            {"TransitionKey", type text},
            {"IncidentKey", type text},
            {"StatusSequence", Int64.Type},
            {"FromStatusId", type text},
            {"FromStatusName", type text},
            {"ToStatusId", type text},
            {"ToStatusName", type text},
            {"ChangedByOperatorId", type text},
            {"ValidFromAt", type datetimezone},
            {"ValidToAt", type datetimezone},
            {"DurationHours", type number},
            {"Reason", type text}
        }
    )
in
    Typed

// Query name: FactAssignmentTransition
let
    Source = Csv.Document(
        File.Contents(LifecycleImportRoot & "\FactAssignmentTransition.csv"),
        [Delimiter = ",", Encoding = 65001, QuoteStyle = QuoteStyle.Csv]
    ),
    PromotedHeaders = Table.PromoteHeaders(Source, [PromoteAllScalars = true]),
    Typed = Table.TransformColumnTypes(
        PromotedHeaders,
        {
            {"TransitionKey", type text},
            {"IncidentKey", type text},
            {"AssignmentSequence", Int64.Type},
            {"FromOperatorGroupId", type text},
            {"FromOperatorGroupName", type text},
            {"OperatorGroupId", type text},
            {"OperatorGroupName", type text},
            {"FromOperatorId", type text},
            {"FromOperatorName", type text},
            {"OperatorId", type text},
            {"OperatorName", type text},
            {"ChangedByOperatorId", type text},
            {"ValidFromAt", type datetimezone},
            {"ValidToAt", type datetimezone},
            {"DurationHours", type number},
            {"Reason", type text}
        }
    )
in
    Typed
