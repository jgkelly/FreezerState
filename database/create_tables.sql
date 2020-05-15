-- SQL Server Table create script

/****** Object:  Table [dbo].[AlarmTypes]    Script Date: 5/15/2020 3:45:42 PM ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[AlarmTypes](
	[Id] [int] NOT NULL,
	[Name] [nvarchar](50) NOT NULL,
PRIMARY KEY CLUSTERED 
(
	[Id] ASC
)WITH (STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO

/****** Object:  Table [dbo].[Location]    Script Date: 5/15/2020 3:46:12 PM ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[Location](
	[Id] [int] NOT NULL,
	[Name] [nvarchar](100) NOT NULL,
PRIMARY KEY CLUSTERED 
(
	[Id] ASC
)WITH (STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO

/****** Object:  Table [dbo].[Readings]    Script Date: 5/15/2020 3:46:53 PM ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[Readings](
	[Id] [int] NOT NULL,
	[LocationId] [int] NOT NULL,
	[Time] [datetime] NOT NULL,
	[Temperature] [int] NOT NULL,
	[AlertId] [int] NULL,
PRIMARY KEY CLUSTERED 
(
	[Id] ASC
)WITH (STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO

ALTER TABLE [dbo].[Readings]  WITH CHECK ADD  CONSTRAINT [FK_AlarmTypes] FOREIGN KEY([AlertId])
REFERENCES [dbo].[AlarmTypes] ([Id])
ON UPDATE CASCADE
ON DELETE CASCADE
GO

ALTER TABLE [dbo].[Readings] CHECK CONSTRAINT [FK_AlarmTypes]
GO

ALTER TABLE [dbo].[Readings]  WITH CHECK ADD  CONSTRAINT [FK_Locations] FOREIGN KEY([LocationId])
REFERENCES [dbo].[Location] ([Id])
ON UPDATE CASCADE
ON DELETE CASCADE
GO

ALTER TABLE [dbo].[Readings] CHECK CONSTRAINT [FK_Locations]
GO

INSERT INTO [dbo].[AlarmTypes] (Id, Name)
VALUES(1, 'High'), (2, 'Low'), (3, 'Status Update')
GO