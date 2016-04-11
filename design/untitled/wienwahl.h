#ifndef WIENWAHL_H
#define WIENWAHL_H

#include <QMainWindow>

namespace Ui {
class Wienwahl;
}

class Wienwahl : public QMainWindow
{
    Q_OBJECT

public:
    explicit Wienwahl(QWidget *parent = 0);
    ~Wienwahl();

private:
    Ui::Wienwahl *ui;
};

#endif // WIENWAHL_H
