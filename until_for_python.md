## 给python添加until语句

目标 －－ demo

```
num = 4
until num == 0:
    print(num)
    num -= 1
```

Grammar/Grammar

*定义语法支持*

```
-compound_stmt: if_stmt | while_stmt | for_stmt | try_stmt | with_stmt | funcdef | classdef | decorated | async_stmt
+compound_stmt: if_stmt | until_stmt | while_stmt | for_stmt | try_stmt | with_stmt | funcdef | classdef | decorated | async_stmt
```

```
+until_stmt: 'until' test ':' suite
 while_stmt: 'while' test ':' suite ['else' ':' suite]
```

Parser/Python.asdl

*定义AST*

```
+          | Until(expr test, stmt* body)
           | While(expr test, stmt* body, stmt* orelse)
```

Python/Python-ast.c

```
+static stmt_ty
+ast_for_until_stmt(struct compiling *c, const node *n)
+{
+    /* until_stmt: 'until' test ':' suite */
+    REQ(n, until_stmt);
+
+    if (NCH(n) == 4) {
+        expr_ty expression;
+        asdl_seq *suite_seq;
+
+        expression = ast_for_expr(c, CHILD(n, 1));
+        if (!expression)
+            return NULL;
+        suite_seq = ast_for_suite(c, CHILD(n, 3));
+        if (!suite_seq)
+            return NULL;
+        return Until(expression, suite_seq, LINENO(n), n->n_col_offset, c->c_arena);
+    }
+
+    PyErr_Format(PyExc_SystemError,
+                 "wrong number of tokens for 'until' statement: %d",
+                 NCH(n));
+    return NULL;
+}
```

```
+            case until_stmt:
+                return ast_for_until_stmt(c, ch);
             case while_stmt:
                 return ast_for_while_stmt(c, ch);
```

Python/compile.c

*AST编译字节码*

```
+static int
+compiler_until(struct compiler *c, stmt_ty s)
+{
+    basicblock *loop, *end, *anchor = NULL;
+    int constant = expr_constant(c, s->v.Until.test);
+
+    if (constant == 1) {
+        return 1;
+    }
+    loop = compiler_new_block(c);
+    end = compiler_new_block(c);
+    if (constant == -1) {
+        anchor = compiler_new_block(c);
+        if (anchor == NULL)
+            return 0;
+    }
+    if (loop == NULL || end == NULL)
+        return 0;
+
+    ADDOP_JREL(c, SETUP_LOOP, end);
+    compiler_use_next_block(c, loop);
+    if (!compiler_push_fblock(c, LOOP, loop))
+        return 0;
+    if (constant == -1) {
+        VISIT(c, expr, s->v.Until.test);
+        ADDOP_JABS(c, POP_JUMP_IF_TRUE, anchor);
+    }
+    VISIT_SEQ(c, stmt, s->v.Until.body);
+    ADDOP_JABS(c, JUMP_ABSOLUTE, loop);
+
+    if (constant == -1) {
+        compiler_use_next_block(c, anchor);
+        ADDOP(c, POP_BLOCK);
+    }
+    compiler_pop_fblock(c, LOOP, loop);
+    compiler_use_next_block(c, end);
+
+    return 1;
+}
```

```
+    case Until_kind:
+        return compiler_until(c, s);
     case While_kind:
         return compiler_while(c, s);
```

Python/symtable.c

*加入符号表*

```
+    case Until_kind:
+        VISIT(st, expr, s->v.Until.test);
+        VISIT_SEQ(st, stmt, s->v.Until.body);
+        break;
     case While_kind:
         VISIT(st, expr, s->v.While.test);
         VISIT_SEQ(st, stmt, s->v.While.body);
         if (s->v.While.orelse)
             VISIT_SEQ(st, stmt, s->v.While.orelse);
         break;
```



