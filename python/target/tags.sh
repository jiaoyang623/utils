cd `ls | grep 360Video`
cd 360Video
cp -r /opt/zygote/360Video/tags/* ./
sed -i 's/\\\\/\//g' project.properties
./genbuild.sh
python changeLog.py ${needProguard} ${needLog}

if [ -e ../../replace_file ]
then
	mv ../../replace_file ./${replace_file}
    unzip -o ${replace_file}
    rm ${replace_file}
fi

/opt/zygote/360Video/utils/makeClone.py
if [ "${isClone}" = "true" ]; then 
	mv ant.properties.clone ant.properties; 
else 
	mv ant.properties.normal ant.properties;
fi

ant -f autobuild.xml clean
ant -f autobuild.xml build -Dmarket_channels="`python /opt/utils/gennum.py "${channels}"`" -DneedLogService="${needLog}" -DneedCheckUpdate="${needCheckUpdate}" -DisClone="${isClone}"

if [ "${isClone}" = "true" ]; then 
	cd build
    for x in `ls`; do /opt/zygote/360Video/utils/jiagu.py $x; done
    cd -
fi

python /opt/zygote/360Video/validation/validate.py build
mv result.csv build/
7z a build/360Video_${version}_`date "+%Y%m%d-%H%M%S"`.7z build/*
rm build/*.apk build/*.csv
if $needExport ; then
datestr=`date "+%Y-%m-%d_%H%M"`;
targetPath=/opt/package/360Video/${version}/${datestr};
mkdir -p ${targetPath};
mv build/* ${targetPath};
fi
