#### 1. Generate a Test World

**Windows (PowerShell):**
```powershell
python make_vacuum_world.py 5 7 0.15 3 | Out-File -Encoding utf8 sample.txt
```

#### 2. Run the Planner

**Uniform-Cost Search:**
```bash
python planner.py uniform-cost sample.txt
```

**Depth-First Search:**
```bash
python planner.py depth-first sample.txt
```
