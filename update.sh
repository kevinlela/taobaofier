rm ./pic_mover.command
touch ./pic_mover.command

echo "cd $(pwd)" >> ./pic_mover.command
echo "sudo python ./pic_mover.py" >> ./pic_mover.command