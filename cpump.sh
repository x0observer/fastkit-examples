start_date="2024-01-14"
days=365

for i in $(seq 0 $days); do
    commit_date=$(date -v+${i}d +"%Y-%m-%d %H:%M:%S")

    # Генерируем случайное количество коммитов (от 1 до 5)
    commits_per_day=$((1 + RANDOM % 5))

    for j in $(seq 1 $commits_per_day); do
        echo "Commit on $commit_date #$j" >> progress.txt
        git add progress.txt
        GIT_COMMITTER_DATE="$commit_date" git commit --date "$commit_date" -m "Commit from $commit_date (#$j)"
    done

    # Делаем случайный отступ (0-2 дня)
    ((i+=RANDOM % 3))
done