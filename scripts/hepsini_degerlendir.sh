for v in baseline A B C; do for s in 1 2 3 4; do
  PYTHONIOENCODING=utf-8 .venv/Scripts/python.exe scripts/degerlendir_v2.py --model models/ppo_${v}_seed$s.zip --etiket ${v}_seed$s 2>&1 | grep -v -i warn &
done; done; wait
