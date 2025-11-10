# UX Pattern Library

## Loading States

**Understand project's loading state patterns first, then check**:

**Loading States** (aligned with project pattern):

```typescript
// Check: Are loading states aligned with project patterns?
// BAD - No loading state (flag if users confused)
function UserList() {
  const [users, setUsers] = useState([]);
  useEffect(() => { fetchUsers().then(setUsers); }, []);
  return users.map(u => <User key={u.id} user={u} />);
}

// GOOD - With loading state (aligned with project Skeleton pattern)
import { Skeleton } from '@/components/ui/Skeleton';

function UserList() {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    setLoading(true);
    fetchUsers()
      .then(setUsers)
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <Skeleton count={5} />;
  return users.map(u => <User key={u.id} user={u} />);
}
```

## Error Messages

**Understand project's error handling patterns first, then check**:

**Error Messages** (aligned with project pattern):

```typescript
// Check: Are error messages aligned with project patterns?
// BAD - Technical error (flag if users confused)
catch (error) {
  alert(error.message); // "ERR_CONNECTION_REFUSED"
}

// GOOD - User-friendly error (aligned with project Toast pattern)
import { toast } from '@/components/ui/Toast';

catch (error) {
  toast.error({
    title: "Couldn't load your profile",
    message: "Please check your internet connection and try again.",
    action: { label: "Retry", onClick: retry }
  });
}
```

## Form Validation

**Understand project's form validation patterns first, then check**:

**Form Validation** (aligned with project pattern):

```typescript
// Check: Is validation aligned with project patterns?
// BAD - Validation only on submit (flag if frustrating)
<form onSubmit={handleSubmit}>
  <input name="email" />
  {/* User fills entire form, clicks submit, sees all errors at once */}
</form>

// GOOD - Inline validation (aligned with project React Hook Form + Zod pattern)
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';

const schema = z.object({
  email: z.string().email('Invalid email address')
});

function Form() {
  const { register, formState: { errors } } = useForm({
    resolver: zodResolver(schema)
  });

  return (
    <form>
      <input {...register('email')} />
      {errors.email && (
        <span className="error">{errors.email.message}</span>
      )}
    </form>
  );
}
```

## Action Feedback

**Understand project's feedback patterns first, then check**:

**Action Feedback** (aligned with project pattern):

```typescript
// Check: Is feedback aligned with project patterns?
// BAD - No feedback (flag if users don't know action succeeded)
<button onClick={handleSave}>Save</button>

// GOOD - Success feedback (aligned with project Toast pattern)
import { toast } from '@/components/ui/Toast';

function SaveButton() {
  const handleSave = async () => {
    await save();
    toast.success('Saved successfully!');
  };

  return <button onClick={handleSave}>Save</button>;
}
```

## Touch Targets (Mobile)

**Understand project's mobile patterns first, then check**:

**Touch Targets** (only flag if prevents interaction):

- Minimum 44x44px (iOS HIG)
- Adequate spacing between tappable elements
- Flag ONLY if users can't tap buttons/links

## Consistency

**Understand project's consistency patterns first, then check**:

**Consistency** (only flag if prevents finding functionality):

- Use consistent button styles (aligned with project patterns)
- Maintain uniform spacing (aligned with project spacing system)
- Follow established patterns (aligned with project design system)
- Flag ONLY if inconsistency confuses users about how to use functionality
