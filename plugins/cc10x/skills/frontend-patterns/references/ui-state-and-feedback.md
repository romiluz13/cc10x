# UI State And Feedback

## Table of Contents
- [State Order](#state-order)
- [Skeletons Versus Spinners](#skeletons-versus-spinners)
- [Error Hierarchy](#error-hierarchy)
- [Empty And Success States](#empty-and-success-states)
- [Mutation Feedback](#mutation-feedback)
- [Checklist](#checklist)

## State Order

Use this order unless the product explicitly requires something else:

```tsx
if (error) return <ErrorState />;
if (loading && !data) return <LoadingState />;
if (!data?.length) return <EmptyState />;
return <SuccessState />;
```

Golden rule: show a loading placeholder only when there is no usable data yet.

## Skeletons Versus Spinners

Use a skeleton when:
- the content shape is known
- the screen is list or card heavy
- the user benefits from spatial continuity

Use a spinner when:
- the shape is unknown
- the action is small and local
- the user is waiting on a button or modal action

## Error Hierarchy

Choose the smallest truthful error surface:
- inline error for field validation
- toast for recoverable background action
- banner for page-level data failure with partial usefulness
- full-screen error when the task cannot continue

Every error state should answer:
- what failed
- what the user can do next

## Empty And Success States

Empty states should:
- explain why the area is empty
- offer the next useful action
- avoid looking like a broken screen

Success states should:
- confirm the action happened
- avoid relying on color alone
- not disappear so quickly that the user misses them

## Mutation Feedback

For async user actions:
- disable double-submit paths
- show progress on the initiating control
- wire an `onError` path with user-visible feedback
- restore the control cleanly after success or failure

## Checklist

Before shipping a UI state machine:
- error is handled
- loading is truthful
- empty state exists for collections
- success feedback exists for mutations
- retry path is obvious where recovery is possible
