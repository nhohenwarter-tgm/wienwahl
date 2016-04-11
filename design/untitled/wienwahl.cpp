#include "wienwahl.h"
#include "ui_wienwahl.h"

Wienwahl::Wienwahl(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::Wienwahl)
{
    ui->setupUi(this);
}

Wienwahl::~Wienwahl()
{
    delete ui;
}
