---
name: Codebase Navigation
description: |
  Provides efficient strategies for exploring codebases, finding relevant code, understanding patterns, and mapping dependencies. Use when analyzing existing code structure and discovering patterns.
  
  Trigger phrases: "find code", "explore codebase", "where is", "locate code",
  "search for", "understand codebase", "code navigation", "find pattern",
  "map dependencies", "discover patterns", "analyze structure", "find similar",
  "locate feature", "understand architecture", "code exploration".
  
  Activates on: context analysis, pattern discovery, architecture understanding,
  dependency mapping, similar feature identification, codebase exploration.
progressive: true
---

# Codebase Navigation

## Progressive Loading Stages

### Stage 1: Metadata (startup - ~50 tokens)
- **Skill**: Codebase Navigation
- **Purpose**: Efficient code exploration and pattern discovery
- **When**: Before implementing features, fixing bugs, understanding architecture
- **Core Rule**: Understand before you change. Find patterns before you code.
- **Sections Available**: Quick Search Patterns, Navigation Strategies, Integration Points

---

### Stage 2: Quick Reference (triggered - ~500 tokens)

#### Quick Search Patterns

**Find similar features**:
```bash
grep -ri "auth\|login" src/ --include="*.ts" | head -10
find src/ -name "*auth*" -type f
```

**Find specific patterns**:
```bash
grep -r "class.*Service" src/ --include="*.ts"
grep -r "export.*function" src/ --include="*.ts"
```

**Find usage**:
```bash
grep -r "from.*UserService\|import.*UserService" src/
grep -r "validateEmail" src/
```

#### Orientation (2 minutes)
```bash
# 1. View structure
tree -L 2 -I 'node_modules|dist|build'
ls -la src/

# 2. Check tech stack
cat package.json | grep "dependencies" -A 20

# 3. Find entry points
find . -name "main.ts" -o -name "index.ts" -o -name "app.ts"
```

#### Pattern Discovery
```
1. Find similar feature (grep)
2. Read main file
3. Note: naming, structure, patterns
4. Follow same approach
```

#### Integration Points Quick Check
```bash
# Database
cat prisma/schema.prisma
grep -r "model User\|interface User" src/

# API
grep -r "router\|@Get\|@Post" src/ | head -10

# External services
cat package.json | grep "stripe\|sendgrid\|aws"
```

#### Navigation Anti-Patterns
- ❌ Read every file sequentially
- ❌ Guess file locations
- ❌ Ignore existing patterns
- ❌ Skip tests
- ✅ Search before browsing
- ✅ Read tests first
- ✅ Find patterns before implementing

---

### Stage 3: Detailed Content (on-demand - ~2500 tokens)

## Detailed Navigation Guide

### Quick Codebase Orientation

#### Step 1: Find Entry Points

**For web applications**:
```bash
# Find main application entry
find . -name "main.ts" -o -name "index.ts" -o -name "app.ts" | head -5

# Find routing/API definitions
grep -r "Router\|createServer\|express()" --include="*.ts" --include="*.js"
```

**For libraries**:
```bash
# Find package entry point
cat package.json | grep "main\|exports"

# Find public API
find . -name "index.ts" -path "*/src/*" | head -5
```

#### Step 2: Understand Structure

```bash
# View directory structure (2 levels deep)
tree -L 2 -I 'node_modules|dist|build'

# Find major directories
ls -la src/
```

**Common patterns**:
- `src/features/` - Feature-based organization
- `src/modules/` - Module-based organization
- `src/components/` - Component-based (frontend)
- `src/services/` - Service layer
- `src/api/` or `src/routes/` - API endpoints
- `src/lib/` or `src/utils/` - Shared utilities

#### Step 3: Check Tech Stack

```bash
# View dependencies
cat package.json | grep "dependencies" -A 20

# Check configuration files
ls -la | grep "config\|rc"
```

## Finding Similar Features

### Strategy: Keyword Search

```bash
# Find feature by name (case-insensitive)
grep -ri "authentication\|auth" src/ --include="*.ts" --include="*.js" | head -10

# Find specific patterns
grep -r "async.*login\|function.*login" src/ --include="*.ts"

# Find class definitions
grep -r "class.*Service\|class.*Controller" src/ --include="*.ts"
```

### Strategy: File Name Search

```bash
# Find files by name pattern
find src/ -name "*auth*" -type f
find src/ -name "*user*" -type f
find src/ -name "*.service.ts"

# Find test files
find . -name "*.test.ts" -o -name "*.spec.ts" | head -10
```

### Strategy: Import Analysis

```bash
# Find what imports a module
grep -r "from.*user.service\|require.*user.service" src/

# Find where a function is used
grep -r "validateEmail\|validatePassword" src/
```

## Understanding Patterns

### Identify Project Conventions

**Step 1: Sample multiple files**
```bash
# Look at 3 service files
find src/ -name "*.service.ts" | head -3 | xargs cat
```

**Step 2: Note patterns**
- **Naming**: `userService` vs `UserService` vs `user-service`
- **Structure**: Class-based vs function-based
- **Exports**: Named vs default
- **Error handling**: Try-catch vs error objects
- **Async**: Promises vs async-await

**Step 3: Follow the pattern**

If you see:
```typescript
// Pattern found in existing code
export class UserService {
  constructor(private db: Database) {}

  async findById(id: string): Promise<User> {
    const user = await this.db.users.findOne({ id });
    if (!user) {
      throw new NotFoundError(`User not found: ${id}`);
    }
    return user;
  }
}
```

Then follow:
```typescript
// Your new code following pattern
export class OrderService {
  constructor(private db: Database) {}

  async findById(id: string): Promise<Order> {
    const order = await this.db.orders.findOne({ id });
    if (!order) {
      throw new NotFoundError(`Order not found: ${id}`);
    }
    return order;
  }
}
```

### Find Testing Patterns

```bash
# Look at existing tests
find . -name "*.test.ts" | head -1 | xargs cat
```

**Note**:
- **Test framework** (Jest, Vitest, Mocha)
- **Test structure** (describe/it vs test)
- **Mock patterns**
- **Setup/teardown** approach

**Follow existing test patterns exactly.**

## Mapping Dependencies

### Direct Dependencies

```bash
# Find what a file imports
head -20 src/features/auth/auth.service.ts | grep "import"

# Find all imports in a feature
grep -h "^import" src/features/auth/*.ts | sort | uniq
```

### Reverse Dependencies

```bash
# Find what depends on this module
grep -r "from.*auth.service" src/ --include="*.ts"

# Find all usages of a function
grep -r "authenticateUser" src/ --include="*.ts"
```

### Dependency Graph (Mental Model)

For feature "User Authentication":

```
1. Find the feature:
   src/features/auth/

2. What does it import? (dependencies)
   - Database (src/shared/database)
   - Logger (src/shared/logger)
   - JWT utility (src/lib/jwt)

3. What imports it? (dependents)
   - API routes (src/api/routes.ts)
   - Middleware (src/middleware/auth.ts)
   - User service (src/features/users/user.service.ts)

4. Integration points:
   - Database: users table
   - Environment: JWT_SECRET config
   - External: Email service (for verification)
```

## Finding Integration Points

### Database Integration

```bash
# Find database schema/models
find . -name "*schema*" -o -name "*model*" | grep -v node_modules | head -10

# Find database queries
grep -r "SELECT\|INSERT\|UPDATE\|DELETE" src/ --include="*.ts" | head -5

# Find ORM usage (Prisma example)
grep -r "prisma\." src/ --include="*.ts" | head -10
```

### API Integration

```bash
# Find API route definitions
grep -r "router\.\|app\.\|@Get\|@Post" src/ --include="*.ts" | head -10

# Find API endpoints
grep -r "'/api\|'/v1" src/ --include="*.ts"
```

### External Service Integration

```bash
# Find external API calls
grep -r "fetch(\|axios\|http\." src/ --include="*.ts" | head -10

# Find third-party service usage
grep -r "stripe\|sendgrid\|aws\|firebase" src/ --include="*.ts"
```

## Efficient Search Strategies

### Strategy 1: Top-Down (Start Broad)

```
1. Understand overall structure (tree -L 2)
2. Find feature area (find by name)
3. Read main file
4. Follow imports to understand dependencies
```

**Use when**: New to codebase, exploring large feature

### Strategy 2: Bottom-Up (Start Specific)

```
1. Search for specific term (grep)
2. Read that file
3. Search for what uses it (reverse grep)
4. Map the flow
```

**Use when**: Looking for specific functionality, debugging

### Strategy 3: Example-Based (Find Similar)

```
1. Find existing similar feature
2. Read its implementation
3. Identify its dependencies
4. Copy the pattern
```

**Use when**: Implementing new feature similar to existing one

## Reading Code Efficiently

### Scan Before Deep Read

```typescript
// Quick scan: Read signatures only
// 1. Exports (public API)
export class UserService {
  // 2. Constructor (dependencies)
  constructor(private db: Database, private logger: Logger) {}

  // 3. Public methods (capabilities)
  async createUser(data: CreateUserInput): Promise<User> { ... }
  async findById(id: string): Promise<User> { ... }
  async updateUser(id: string, data: UpdateUserInput): Promise<User> { ... }
  async deleteUser(id: string): Promise<void> { ... }

  // 4. Private methods (implementation details - skip for now)
  private async validateUserData(data: any) { ... }
  private async hashPassword(password: string) { ... }
}
```

**First pass**: Exports, constructor, public methods only

**Second pass**: Implementation details only if needed

### Focus on Test Files

```typescript
// Tests reveal intended behavior
describe('UserService', () => {
  describe('createUser', () => {
    it('creates user with hashed password', async () => {
      // This test tells you: createUser hashes passwords
    });

    it('throws ValidationError for invalid email', async () => {
      // This test tells you: createUser validates emails
    });

    it('throws ConflictError for duplicate email', async () => {
      // This test tells you: createUser checks duplicates
    });
  });
});
```

**Tests answer**: What does this do? What are edge cases? What can go wrong?

## Common Navigation Patterns

### Pattern: "Where is X defined?"

```bash
# For functions
grep -r "function getUser\|const getUser\|export.*getUser" src/

# For classes
grep -r "class UserService\|export class UserService" src/

# For types
grep -r "interface User\|type User" src/
```

### Pattern: "Where is X used?"

```bash
# Find usages
grep -r "UserService\|getUser" src/ --include="*.ts" | grep -v "^.*:.*//\|/\*"

# Exclude comments, focus on actual usage
```

### Pattern: "What depends on this file?"

```bash
# Find imports of specific file
grep -r "from.*user.service\|require.*user.service" src/
```

### Pattern: "How does feature X work?"

```
1. Find entry point: grep -r "router.*user\|@Controller.*user" src/
2. Read route handler
3. Follow to service layer
4. Follow to database layer
5. Check tests for behavior
```

## Tools Quick Reference

```bash
# File finding
find <path> -name "<pattern>" -type f

# Content search
grep -r "<pattern>" <path> --include="*.ts"

# Case-insensitive search
grep -ri "<pattern>" <path>

# Show context (3 lines before/after)
grep -r "<pattern>" <path> -C 3

# Count occurrences
grep -r "<pattern>" <path> -c

# List files with matches only
grep -r "<pattern>" <path> -l

# Exclude directories
grep -r "<pattern>" --exclude-dir=node_modules --exclude-dir=dist

# Directory structure
tree -L <depth> -I 'node_modules|dist|build'

# File content with line numbers
cat -n <file>

# First N lines
head -<N> <file>

# Last N lines
tail -<N> <file>
```

## Quick Start Guide

When starting on a new task:

```
Step 1: Orient (2 minutes)
- View structure: tree -L 2 src/
- Check tech: cat package.json

Step 2: Find Similar (3 minutes)
- Search: grep -ri "similar_feature" src/
- Read: cat src/path/to/similar-feature.ts

Step 3: Map Dependencies (2 minutes)
- What it imports: head -20 file | grep import
- What imports it: grep -r "from.*file" src/

Step 4: Understand Patterns (3 minutes)
- Read tests: cat similar-feature.test.ts
- Note conventions: naming, structure, errors

Total: 10 minutes of navigation before coding
Result: Clear implementation path, following patterns
```

## Remember

**Efficient navigation means**:
- ✅ Search before browsing
- ✅ Read tests before code
- ✅ Find patterns before implementing
- ✅ Map dependencies before integrating

**Inefficient navigation means**:
- ❌ Reading files sequentially
- ❌ Guessing where things are
- ❌ Ignoring existing patterns
- ❌ Coding before understanding

**10 minutes of navigation saves hours of debugging.**
