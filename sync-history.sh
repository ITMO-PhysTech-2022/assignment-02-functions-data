RED="\033[0;31m"
NC="\033[0m"

dir=$(basename "$PWD")
if [[ "$dir" =~ ^assignment-[0-9]{2}-.*$ ]]; then
  IFS="-" read -ra parts <<<"$dir"
  echo "Задание номер ${parts[1]}"
else
  echo -e "${RED}Кажется, вы не находитесь в папке задания (assignment-XX-yyy-ваш-ник)${NC}"
  echo "Используйте команду cd, чтобы переместиться в нужную папку"
  exit
fi

key_files=(~/.ssh/id_*)
keys=()
for key_file in "${key_files[@]}"; do
  # shellcheck disable=SC2207
  keys+=($(basename "$key_file"))
done

if [ -e "${key_files[0]}" ]; then
  echo "Найдены SSH-ключи: ${keys[*]}"
  upstream="${parts[0]}-${parts[1]}-${parts[2]}-${parts[3]}"

  echo -e "${RED}Убедитесь, что папка '${dir}' имеет имя assignment-XX-yyy-ваш-ник${NC}"
  echo -e "${RED}Убедитесь, что '${upstream}' - это то же самое без вашего ника${NC}"
  echo "Если это не так, остановите скрипт и склонируйте репозиторий нормально"
  while true; do
    # shellcheck disable=SC2162
    read -p "Продолжить? [yn] " yn
    case $yn in
    [yY]*) break ;;
    [nN]*)
      echo "Ok, перезапустите скрипт, если будете готовы :("
      exit
      ;;
    *) echo "Ответьте y (yes) или n (no)" ;;
    esac
  done

  change_to_ssh() {
    git remote set-url origin "git@github.com:ITMO-PhysTech-2022/${dir}"
    echo -e "${RED}Репозиторий origin перенастроен на доступ по SSH${NC}"
  }

  rewrite_history() {
    git checkout main
    git remote add upstream "git@github.com:ITMO-PhysTech-2022/${upstream}"
    git fetch --all
    git reset --hard upstream/main ||
      echo -e "${RED}Что-то пошло не так, перезапустите скрипт или напишите @doreshnikov${NC}"
    git push --force origin main ||
      echo -e "${RED}Что-то пошло не так, перезапустите скрипт или напишите @doreshnikov${NC}"
    echo -e "${RED}Проверьте историю в вашем репозитории на GitHub${NC}"
    echo "Если что-то не так, пишите @doreshnikov"
  }

  while true; do
    echo -e "${RED}Ваши коммиты ветки main будут (не)безвозвратно утеряны${NC}"
    # shellcheck disable=SC2162
    read -p "Переписать историю через основной репозиторий? [yn] " yn
    case $yn in
    [yY]*)
      change_to_ssh
      rewrite_history
      break
      ;;
    [nN]*)
      echo "Ok, перезапустите скрипт, если будете готовы :("
      exit
      ;;
    *) echo "Ответьте y (yes) или n (no)" ;;
    esac
  done
else
  echo "SSH-ключи не найдены :("
  # shellcheck disable=SC2162

  generate_key() {
    echo "Следующие три раза просто нажмите Enter"
    ssh-keygen
    echo -e "${RED}
1. Найдите в папке ${HOME}/.ssh .pub-файл с выведенным выше именем
2. Откройте его с помощью блокнота и скопируйте
3. Откройте https://github.com/settings/keys
4. Нажмите 'New SSH key', вставьте скопированные данные, сохраните
5. Перезапустите этот скрипт${NC}"
  }

  while true; do
    # shellcheck disable=SC2162
    read -p "Сгенерировать новый? [yn] " yn
    case $yn in
    [yY]*)
      generate_key
      break
      ;;
    [nN]*)
      echo "Ok, перезапустите скрипт, если будете готовы :("
      exit
      ;;
    *) echo "Ответьте y (yes) или n (no)" ;;
    esac
  done
fi
