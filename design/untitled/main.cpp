#include "wienwahl.h"
#include <QApplication>

int main(int argc, char *argv[])
{
    QApplication a(argc, argv);
    Wienwahl w;
    w.show();

    return a.exec();
}
